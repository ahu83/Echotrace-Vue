export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Serve assets (JS, CSS, images, etc.)
    if (url.pathname.match(/\.[^/]+$/)) {
      return env.ASSETS.fetch(request);
    }

    // For all other paths (like /signup, /login, /tts, etc.), return index.html
    return env.ASSETS.fetch(`${url.origin}/index.html`);
  },
};