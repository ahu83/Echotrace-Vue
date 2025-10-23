<template>
  <div class="page history">
    <side-panel @signout="onSignout" />

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel">

        <div class="head">
          <h2 class="title">AI Generation History</h2>
          <button class="pill" @click="exportCsv">Export CSV</button>
        </div>


        <div class="filters">
          <el-input
            v-model="q.keyword"
            placeholder="Search by title / id / model"
            clearable
            style="width:240px"
            @keyup.enter.native="applyFilters"
          />
          <el-select
            v-model="q.type"
            placeholder="Type"
            clearable
            style="width:150px"
          >
            <el-option label="All" value="" />
            <el-option label="Text-To-Speech" value="tts" />
            <el-option label="Detection" value="detect" />
            <el-option label="Watermark" value="wm" />
          </el-select>
          <el-select
            v-model="q.status"
            placeholder="Status"
            clearable
            style="width:150px"
          >
            <el-option label="All" value="" />
            <el-option label="Processing" value="PROCESSING" />
            <el-option label="Success" value="SUCCESS" />
            <el-option label="Failed" value="FAILED" />
          </el-select>
          <el-button type="primary" @click="applyFilters">Search</el-button>
          <el-button @click="reset">Reset</el-button>
        </div>


        <el-table
          :data="pageItems"
          @selection-change="sels = $event"
          height="480"
          style="width: 100%"
        >
          <el-table-column type="selection" width="45" />
          <el-table-column label="Type" width="240">
            <template slot-scope="s">
              <el-tag size="small" :type="typeTagType(s.row.type)">
                {{ typeLabel(s.row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="Title" min-width="240" />
          <el-table-column label="Created" width="240">
            <template slot-scope="s">
              {{ formatDate(s.row.createdAt) }}
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="220" fixed="right">
            <template slot-scope="s">
              <el-button type="text" @click="view(s.row)">View</el-button>
              <el-button
                type="text"
                @click="download(s.row)"
                :disabled="!s.row.url"
              >
                Download
              </el-button>
              <el-button type="text" @click="remove(s.row)">Delete</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </section>

    <el-dialog title="Preview" :visible.sync="dlg.visible" width="720px">
      <div v-if="dlg.item && dlg.item.type === 'tts'">
        <audio :src="dlg.item.url" controls style="width: 100%"></audio>
      </div>
      <div v-else-if="dlg.item && dlg.item.type === 'detect'">
        <p style="margin: 0 0 12px;">Open detection result page?</p>
        <el-button type="primary" @click="$router.push('/result')">
          Go to result
        </el-button>
      </div>
      <div v-else>
        <pre class="json">{{ pretty(dlg.item) }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import SidePanel from "@/components/SidePanel.vue";

export default {
  name: "AiHistory",
  components: { SidePanel },
  data() {
    return {
      q: { keyword: "", type: "", status: "", page: 1, size: 10 },
      list: [],
      sels: [],
      dlg: { visible: false, item: null },
    };
  },
  created() {
    this.fetchData();
  },
  computed: {
    filtered() {
      const { keyword, type, status } = this.q;
      const kw = (keyword || "").toLowerCase();
      let arr = this.list.slice();
      if (kw) arr = arr.filter((r) => `${r.title} ${r.id}`.toLowerCase().includes(kw));
      if (type) arr = arr.filter((r) => r.type === type);
      if (status) arr = arr.filter((r) => r.status === status);
      return arr.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    },
    pageItems() {
      const st = (this.q.page - 1) * this.q.size;
      return this.filtered.slice(st, st + this.q.size);
    },
  },
  methods: {
    onSignout() {
      this.$message("Sign out clicked");
    },
    fetchData() {
      this.list = [
        {
          id: "H24001",
          type: "tts",
          title: "Promo-line 001",
          createdAt: "2025-03-12T10:15:00Z",
          url: "/mock/audio1.mp3",
        },
        {
          id: "H24002",
          type: "detect",
          title: "Call-sample 17",
          createdAt: "2025-03-12T09:40:00Z",
        },
        {
          id: "H24003",
          type: "wm",
          title: "Embed watermark",
          createdAt: "2025-03-11T16:22:00Z",
        },
        {
          id: "H24004",
          type: "tts",
          title: "Narration-A",
          createdAt: "2025-03-10T08:02:00Z",
        },
      ];
    },
    applyFilters() {
      this.q.page = 1;
    },
    reset() {
      this.q = { keyword: "", type: "", status: "", page: 1, size: this.q.size };
    },
    view(row) {
      this.dlg.item = row;
      this.dlg.visible = true;
    },
    download(row) {
      if (!row.url) return;
      const a = document.createElement("a");
      a.href = row.url;
      a.download = row.title || "file";
      a.click();
    },
    remove(row) {
      this.list = this.list.filter((r) => r.id !== row.id);
      this.$message.success("Deleted");
    },
    formatDate(s) {
      return new Date(s).toLocaleString();
    },
    typeLabel(t) {
      return { tts: "Text-To-Speech", detect: "Detection", wm: "Watermark" }[t] || t;
    },
    typeTagType(t) {
      return { tts: "success", detect: "warning", wm: "info" }[t] || "info";
    },
    pretty(o) {
      try {
        return JSON.stringify(o, null, 2);
      } catch {
        return String(o);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000;
$border: rgba(255, 255, 255, .08);
$text: #E6E8EB;
$muted: #AAB2C0;

.history {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
}

.panel-wrap {
  padding-left: 72px;
}

.looper {
  position: fixed;
  top: 200px;
  inset: 0 0 0 72px;
  background: url(~@/assets/looper-bg.png) center / 1600px auto no-repeat;
  opacity: .5;
  transform: rotate(15deg);
  pointer-events: none;
  background-size: 100%;
  background-position: 0px -300px;
}

.panel {
  max-width: 1120px;
  margin: 0 auto 80px;
  background: $panel;
  border: 1px solid $border;
  border-radius: 16px;
  box-shadow: 0 4px 50px rgba(33, 33, 33, .08),
    0 4px 6px rgba(33, 33, 33, .04);
  padding: 18px;
  position: relative;
  top: 100px;
}


.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: #000 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
}

.title {
  margin: 0;
  color: #fff;
  font: 800 28px/1.2 "Cabin", "Segoe UI", Arial, sans-serif;
}

.pill {
  height: 40px;
  padding: 0 18px;
  border-radius: 100px;
  cursor: pointer;
  border: 1.5px solid transparent;
  background-image: linear-gradient(#000, #000),
    linear-gradient(91.06deg, #FF1CF7 2.26%, #00F0FF 100%);
  background-origin: border-box;
  background-clip: padding-box, border-box;
  color: #fff;
  font-weight: 600;
  &:hover {
    opacity: .95;
  }
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 6px;
  background: #000;
  border: 1px solid $border;
  border-radius: 12px;
  margin: 6px 6px 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, .35);
}


::v-deep(.el-table),
::v-deep(.el-table__body-wrapper),
::v-deep(.el-table__fixed-right),
::v-deep(.el-table__fixed-right-patch),
::v-deep(.el-table__fixed),
::v-deep(.el-table__header-wrapper),
::v-deep(.el-table__footer-wrapper) {
  background: #000 !important;
  color: $text !important;
}

::v-deep(.el-table th),
::v-deep(.el-table td) {
  background: #000 !important;
  color: $text !important;
}

::v-deep(.el-table__body tr:hover > td) {
  background: rgba(255, 255, 255, .05) !important;
}

::v-deep(.el-table__fixed-right),
::v-deep(.el-table__fixed) {
  box-shadow: none !important;
  background-color: #000 !important;
}

::v-deep(.el-table__empty-block) {
  background: #000 !important;
  color: rgba(255, 255, 255, .3);
}

/* ✅ Tag colors */
::v-deep(.el-tag--success) {
  background: rgba(16, 185, 129, .18) !important;
  color: #A7F3D0 !important;
}

::v-deep(.el-tag--warning) {
  background: rgba(234, 179, 8, .20) !important;
  color: #FDE68A !important;
}

::v-deep(.el-tag--info) {
  background: rgba(255, 255, 255, .1) !important;
  color: #E6E8EB !important;
}
</style>
