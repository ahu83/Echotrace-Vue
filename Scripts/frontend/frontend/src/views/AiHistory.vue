<template>
  <div class="page history">
    <side-panel @signout="onSignout"/>

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
          <el-select v-model="q.type" placeholder="Type" clearable style="width:150px">
            <el-option label="All" value=""/>
            <el-option label="Text-To-Speech" value="tts"/>
            <el-option label="Detection" value="detect"/>
            <el-option label="Watermark" value="wm"/>
          </el-select>
          <el-select v-model="q.status" placeholder="Status" clearable style="width:150px">
            <el-option label="All" value=""/>
            <el-option label="Processing" value="PROCESSING"/>
            <el-option label="Success" value="SUCCESS"/>
            <el-option label="Failed" value="FAILED"/>
          </el-select>
          <el-button type="primary" @click="applyFilters">Search</el-button>
          <el-button @click="reset">Reset</el-button>
        </div>

        <el-table :data="pageItems" @selection-change="sels = $event" height="480" style="width:100%">
          <el-table-column type="selection" width="45"/>
          <el-table-column label="Type" width="240">
            <template slot-scope="s">
              <el-tag size="small" :type="typeTagType(s.row.type)">{{ typeLabel(s.row.type) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="Title" min-width="240"/>
          <el-table-column label="Created" width="240">
            <template slot-scope="s">{{ formatDate(s.row.createdAt) }}</template>
          </el-table-column>
          <el-table-column label="Actions" width="220" fixed="right">
            <template slot-scope="s">
              <el-button type="text" @click="view(s.row)">View</el-button>
              <el-button type="text" @click="download(s.row)" :disabled="!s.row.url">Download</el-button>
              <el-button type="text" @click="remove(s.row)">Delete</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </section>

    <el-dialog title="Preview" :visible.sync="dlg.visible" width="720px">
      <div v-if="dlg.item && dlg.item.type==='tts'">
        <audio :src="dlg.item.url" controls style="width:100%"></audio>
      </div>
      <div v-else-if="dlg.item && dlg.item.type==='detect'">
        <p style="margin:0 0 12px;">Open detection result page?</p>
        <el-button type="primary" @click="$router.push('/result')">Go to result</el-button>
      </div>
      <div v-else>
        <pre class="json">{{ pretty(dlg.item) }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import SidePanel from '@/components/SidePanel.vue';

export default {
  name: 'AiHistory',
  components: {SidePanel},
  data() {
    return {
      q: {keyword: '', type: '', status: '', range: null, page: 1, size: 10},
      list: [],
      sels: [],
      dlg: {visible: false, item: null}
    };
  },
  created() {
    this.fetchData();
  },
  computed: {
    filtered() {
      const {keyword, type, status, range} = this.q;
      const kw = (keyword || '').toLowerCase();
      let arr = this.list.slice();

      if (kw) arr = arr.filter(r =>
          `${r.title} ${r.id} ${r.model}`.toLowerCase().includes(kw));
      if (type) arr = arr.filter(r => r.type === type);
      if (status) arr = arr.filter(r => r.status === status);
      if (range && range.length === 2) {
        const [s, e] = range;
        const end = new Date(e);
        end.setHours(23, 59, 59, 999);
        arr = arr.filter(r => new Date(r.createdAt) >= new Date(s) && new Date(r.createdAt) <= end);
      }
      return arr.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    },
    pageItems() {
      const st = (this.q.page - 1) * this.q.size;
      return this.filtered.slice(st, st + this.q.size);
    }
  },
  methods: {
    onSignout() {
      this.$message('Sign out clicked');
    },
    async fetchData() {
      this.list = [
        {
          id: 'H24001',
          type: 'tts',
          title: 'Promo-line 001',
          createdAt: '2025-03-12T10:15:00Z',
          url: '/mock/audio1.mp3'
        },
        {
          id: 'H24002',
          type: 'detect',
          title: 'Call-sample 17',
          createdAt: '2025-03-12T09:40:00Z'
        },
        {
          id: 'H24003',
          type: 'wm',
          title: 'Embed watermark',
          createdAt: '2025-03-11T16:22:00Z'
        },
        {
          id: 'H24004',
          type: 'tts',
          title: 'Narration-A',
          createdAt: '2025-03-10T08:02:00Z'
        }
      ];
    },
    applyFilters() {
      this.q.page = 1;
    },
    reset() {
      this.q = {keyword: '', type: '', status: '', range: null, page: 1, size: this.q.size};
    },
    view(row) {
      this.dlg.item = row;
      this.dlg.visible = true;
    },
    download(row) {
      if (!row.url) return;
      const a = document.createElement('a');
      a.href = row.url;
      a.download = row.title || 'file';
      a.click();
    },
    remove(row) {
      this.$confirm('Delete this record?', 'Confirm', {type: 'warning'})
          .then(() => {
            this.list = this.list.filter(r => r.id !== row.id);
            this.$message.success('Deleted');
          })
          .catch(() => {
          });
    },
    exportCsv() {
      const cols = ['id', 'type', 'title', 'model', 'params', 'status', 'createdAt', 'url'];
      const lines = [cols.join(',')].concat(
          this.filtered.map(r => cols.map(k => `"${(r[k] || '').toString().replace(/"/g, '""')}"`).join(','))
      );
      const blob = new Blob([lines.join('\n')], {type: 'text/csv;charset=utf-8;'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'ai_history.csv';
      a.click();
      URL.revokeObjectURL(url);
    },

    formatDate(s) {
      const d = new Date(s);
      return d.toLocaleString();
    },
    typeLabel(t) {
      return {tts: 'Text-To-Speech', detect: 'Detection', wm: 'Watermark'}[t] || t;
    },
    typeTagType(t) {
      return {tts: 'success', detect: 'warning', wm: 'info'}[t] || 'info';
    },
    statusType(s) {
      return {SUCCESS: 'success', PROCESSING: 'warning', FAILED: 'danger'}[s] || 'info';
    },
    pretty(o) {
      try {
        return JSON.stringify(o, null, 2);
      } catch (e) {
        return String(o);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$bg: #0A0A0A;
$panel: #000;
$border: rgba(255, 255, 255, .08);
$text: #E6E8EB;

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
  box-shadow: 0 4px 50px rgba(33, 33, 33, .08), 0 4px 6px rgba(33, 33, 33, .04);
  padding: 18px 18px 10px;
  position: relative;
  top: 100px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 6px 12px;
}

.title {
  margin: 0;
  color: #fff;
  font: 800 28px/1.2 'Cabin', 'Segoe UI', Arial, sans-serif;
}

.pill {
  position: relative;
  height: 40px;
  padding: 0 18px 0 18px;
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
}

.foot {
  display: flex;
  justify-content: flex-end;
  padding: 8px 6px 12px;
}

.json {
  background: #111;
  color: #E6E8EB;
  padding: 12px;
  border-radius: 8px;
}


$bg: #0A0A0A;
$panel: #000;
$text: #E6E8EB;
$muted: #AAB2C0;
$border: rgba(255, 255, 255, .08);

.filters {
  background: #0F0F0F;
  border: 1px solid $border;
  border-radius: 12px;
  padding: 10px 12px;
  margin: 6px 6px 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, .35);
}

::v-deep .el-input__inner,
::v-deep .el-range-editor.el-input__inner,
::v-deep .el-date-editor .el-input__inner {
  background: rgba(19, 19, 22, .8);
  border: 1px solid rgba(255, 255, 255, .14);
  color: $text;
}

::v-deep .el-input__inner::placeholder,
::v-deep .el-range-editor .el-range-input::placeholder {
  color: rgba(230, 232, 235, .55);
}

::v-deep .el-input__icon {
  color: $muted;
}

::v-deep .el-select-dropdown,
::v-deep .el-picker-panel {
  background: #0F0F10;
  border: 1px solid $border;
  color: $text;
}

::v-deep .el-select-dropdown__item.hover,
::v-deep .el-select-dropdown__item.selected {
  background: rgba(255, 255, 255, .06);
  color: #fff;
}

::v-deep .el-table {
  background: transparent;
  color: $text;
}

::v-deep .el-table th,
::v-deep .el-table tr {
  background: transparent;
}

::v-deep .el-table__header th {
  background: rgba(255, 255, 255, .04);
  color: #E6E8EB;
  border-bottom: 1px solid $border;
}

::v-deep .el-table td,
::v-deep .el-table th.is-leaf {
  border-bottom: 1px solid rgba(255, 255, 255, .06);
}

::v-deep .el-table__body tr:hover > td {
  background: rgba(255, 255, 255, .04) !important;
}

::v-deep .el-table__empty-block {
  background: transparent;
  color: $muted;
}

::v-deep .el-tag {
  background: rgba(255, 255, 255, .08);
  border: none;
  color: #E6E8EB;
}

::v-deep .el-tag--success {
  background: rgba(16, 185, 129, .18);
  color: #A7F3D0;
}

::v-deep .el-tag--warning {
  background: rgba(234, 179, 8, .20);
  color: #FDE68A;
}

::v-deep .el-tag--danger {
  background: rgba(239, 68, 68, .22);
  color: #FCA5A5;
}

::v-deep .el-pagination button,
::v-deep .el-pagination .el-pager li {
  background: transparent;
  color: $text;
}

::v-deep .el-pagination .el-pager li.active {
  background: rgba(255, 255, 255, .08);
}

::v-deep .el-dialog {
  background: #0F0F0F;
  color: $text;
  border: 1px solid $border;
}

::v-deep .el-dialog__header {
  border-bottom: 1px solid $border;
}

::v-deep .el-dialog__title {
  color: #fff;
}

.json {
  background: #111;
  color: $text;
}

.foot {
  background: transparent;
}

</style>
