<template>
  <div class="page history">
    <side-panel @signout="onSignout" />

    <div class="looper"></div>

    <section class="panel-wrap">
      <div class="panel">
        <div class="head">
          <h2 class="title">AI Generation History</h2>
        </div>

        <el-table :data="list" height="480" style="width:100%">
          <el-table-column prop="type" label="Type" width="240">
            <template slot-scope="s">
              <el-tag size="small" :type="typeTagType(s.row.type)">
                {{ typeLabel(s.row.type) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="title" label="Title" min-width="240" />
          <el-table-column label="Created" width="240">
            <template slot-scope="s">{{ formatDate(s.row.createdAt) }}</template>
          </el-table-column>

          <el-table-column label="Actions" width="220" fixed="right">
            <template slot-scope="s">
              <el-button type="text" @click="playAudio(s.row)">Play</el-button>
              <el-button type="text" @click="download(s.row)">Download</el-button>
              <el-button type="text" @click="remove(s.row)">Delete</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </section>

    <el-dialog title="Playback" :visible.sync="dlg.visible" width="720px">
      <div v-if="dlg.item">
        <h3>{{ dlg.item.title }}</h3>
        <audio :src="dlg.item.url" controls style="width:100%"></audio>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import SidePanel from "@/components/SidePanel.vue";
import api from "@/api";

export default {
  name: "AiHistory",
  components: { SidePanel },
  data() {
    return {
      list: [],
      dlg: { visible: false, item: null },
      loading: false,
    };
  },
  async mounted() {
    this.fetchHistory();
  },
  methods: {
    onSignout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    },

    async fetchHistory() {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");
        const res = await api.get("/history", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.list = res.data || [];
      } catch (err) {
        console.error("Failed to fetch history:", err);
        this.$message.error("Error loading history");
      } finally {
        this.loading = false;
      }
    },

    playAudio(row) {
      this.dlg.item = row;
      this.dlg.visible = true;
    },

    download(row) {
      if (!row.url) return;
      const a = document.createElement("a");
      a.href = row.url;
      a.download = `${row.title.replace(/\s+/g, "_")}.wav`;
      a.click();
    },

    remove(row) {
      this.$confirm("Delete this record?", "Confirm", { type: "warning" })
        .then(() => {
          this.list = this.list.filter((r) => r.id !== row.id);
          this.$message.success("Deleted (local only)");
        })
        .catch(() => {});
    },

    formatDate(s) {
      const d = new Date(s);
      return d.toLocaleString();
    },

    typeLabel(t) {
      return { tts: "Text-To-Speech", detect: "Detection", wm: "Watermark" }[t] || t;
    },

    typeTagType(t) {
      return { tts: "success", detect: "warning", wm: "info" }[t] || "info";
    },
  },
};
</script>

<style lang="scss" scoped>
$bg: #0a0a0a;
$panel: #000;
$border: rgba(255, 255, 255, 0.08);
$text: #e6e8eb;

.history {
  min-height: 100vh;
  background: $bg;
  color: $text;
  position: relative;
}

.panel-wrap {
  padding-left: 72px;
}

@media (min-width: 992px) {
  .side.expanded + .looper + .panel-wrap {
    padding-left: 226px;
  }
}

.looper {
  position: fixed;
  top: 200px;
  inset: 0 0 0 72px;
  background: url(~@/assets/looper-bg.png) center / 1600px auto no-repeat;
  opacity: 0.5;
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
  box-shadow: 0 4px 50px rgba(33, 33, 33, 0.08),
    0 4px 6px rgba(33, 33, 33, 0.04);
  padding: 18px 18px 10px;
  position: relative;
  top: 100px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #000;
  padding: 8px 6px 12px;
  border-bottom: 1px solid $border;
}

.title {
  margin: 0;
  color: #fff;
  font: 800 28px/1.2 "Cabin", "Segoe UI", Arial, sans-serif;
}


::v-deep .el-table,
::v-deep .el-table__body,
::v-deep .el-table th,
::v-deep .el-table tr,
::v-deep .el-table__empty-block {
  background: #000 !important;
  color: #e6e8eb !important;
}

::v-deep .el-table__header th {
  background: #111 !important;
  color: #fff !important;
}

::v-deep .el-table td,
::v-deep .el-table th.is-leaf {
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

::v-deep .el-table__body tr:hover > td {
  background: rgba(255, 255, 255, 0.04) !important;
}

::v-deep .el-table__empty-text {
  color: #aaa !important;
}

.no-data {
  text-align: center;
  color: #aaa;
  margin-top: 40px;
}
</style>
