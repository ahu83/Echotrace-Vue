export default {
  async fetch(request) {
    const url = new URL(request.url);

    // Proxy API routes to Flask backend on Render
    if (
      url.pathname.startsWith("/api") ||
      url.pathname.startsWith("/login") ||
      url.pathname.startsWith("/register") ||
      url.pathname.startsWith("/verify-token") ||
      url.pathname.startsWith("/profile") ||
      url.pathname.startsWith("/generate") ||
      url.pathname.startsWith("/detect")
    ) {
      url.hostname = "echotrace-vue.onrender.com";
      url.protocol = "https:";

      // Forward method, headers, and body
      const response = await fetch(url.toString(), {
        method: request.method,
        headers: request.headers,
        body: request.method !== "GET" && request.method !== "HEAD" ? request.body : undefined,
      });

      // Add CORS headers
      const newHeaders = new Headers(response.headers);
      newHeaders.set("Access-Control-Allow-Origin", "*");
      newHeaders.set("Access-Control-Allow-Headers", "Authorization, Content-Type");

      return new Response(response.body, { status: response.status, headers: newHeaders });
    }

    // Default: serve frontend normally
    return fetch(request);
  },
};