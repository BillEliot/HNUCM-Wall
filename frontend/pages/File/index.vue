<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>学习资料文件</h1>
                            <p class="subheading"></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12 text-center">
                    <a-select v-model="subject" @change="handleChange" class="col-md-6">
                        <a-select-opt-group>
                            <span slot="label"><a-icon type="heat-map"/>中医类</span>
                            <a-select-option v-for="subject in zySubjects" :key="subject" :value="subject">{{ subject }}</a-select-option>
                        </a-select-opt-group>
                        <a-select-opt-group>
                            <span slot="label"><a-icon type="stock"/>西医类</span>
                            <a-select-option v-for="subject in xySubjects" :key="subject" :value="subject">{{ subject }}</a-select-option>
                        </a-select-opt-group>
                    </a-select>
                    <a-input-search
                        placeholder="当前选择科目下搜索"
                        @search="searchFile"
                        enterButton
                        class="col-md-6"
                    />
                    <!-- --------------------------------------------- -->
                    <div style="margin-top: 50px"></div>
                    <hr />
                    <a-table :columns="columns" :data-source="fileList" :rowKey="fileList => fileList.id" rowKey="name">
                        <a-tag slot="type" slot-scope="text" :color="text === 'word' ? 'blue' : text === 'excel' ? 'green' : text === 'pdf' ? 'red' : 'orange'">
                            {{ text }}
                        </a-tag>
                        <span slot="date" slot-scope="text">
                            {{ moment(text).format('lll') }}
                        </span>
                        <span slot="action" slot-scope="text, record">
                            <a @click="view(record.url, record.id)">查看</a>
                            <a-divider type="vertical" />
                            <a @click="download(record.url, record.id)">下载</a>
                        </span>
                    </a-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
        moment,

        subject: '请选择科目',
        fileList: [],
        columns: [{
            title: '文件',
            dataIndex: 'name',
          }, {
            title: '类型',
            dataIndex: 'type',
            scopedSlots: { customRender: 'type' },
            filters: [
                { text: 'word', value: 'word' },
                { text: 'excel', value: 'excel' },
                { text: 'ppt', value: 'ppt' },
                { text: 'pdf', value: 'pdf' }
            ],
            onFilter: (value, record) => record.type.includes(value)
          }, {
            title: '文件大小',
            dataIndex: 'size',
            sorter: (a, b) => a.sizeSort - b.sizeSort,
          }, {
            title: '上传日期',
            dataIndex: 'date',
            scopedSlots: { customRender: 'date' },
            sorter: (a, b) => {
                if (moment(a.date).isAfter(moment(b.date))) return 1
                else if (moment(a.date).isBefore(moment(b.date))) return -1
                else return 0
            }
          }, {
            title: '下载次数',
            dataIndex: 'downloadCount',
            sorter: (a, b) => a.downloadCount - b.downloadCount,
          }, {
            title: '查看次数',
            dataIndex: 'viewCount',
            sorter: (a, b) => a.viewCount - b.viewCount,
          }, {
            title: '操作',
            scopedSlots: { customRender: 'action' },
        }]
    }
  },
  async asyncData({ $axios }) {
    let zySubjects = []
    let xySubjects = []

    // Get subjects and chapters
    await $axios.get('getFileSubjects')
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            response.data.data.forEach(subject => {
                if (subject.subjectType == 'zy') {
                    zySubjects.push(subject.name)
                }
                else if (subject.subjectType == 'xy') {
                    xySubjects.push(subject.name)
                }
            })
        }
    })

    return {
        zySubjects: zySubjects,
        xySubjects: xySubjects
    }
  },
  methods: {
      handleChange(val) {
          if (this.subject != '请选择科目') {
            this.$axios.get('getFileList', {
                params: {
                    subject: this.subject,
                    keyword: ''
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.fileList = response.data.data
                }
            })
          }
          else {
              this.$message.warning('请选择科目')
          }
      },
      searchFile(val) {
          if (this.subject != '请选择科目') {
            this.$axios.get('getFileList', {
                params: {
                    subject: this.subject,
                    keyword: val
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.fileList = response.data.data
                    this.$notification.open({
                        message: '搜索结果',
                        description: `共搜索到 ${this.fileList.length} 条结果`,
                        icon: <a-icon type="smile" style="color: #108ee9" />,
                        duration: 0
                    })
                }
            })
          }
          else {
            this.$message.warning('请选择科目')
          }
      },
      view(url, id) {
          window.open('http://view.officeapps.live.com/op/view.aspx?src=' + this.baseUrl + url, '_blank')

          this.$axios.get('addFileViewCount', {
              params: {
                  id: id
              }
          })
          this.fileList.forEach((item, index) => {
            if (item.id == id) {
                item.viewCount += 1
                return true
            }
          })
      },
      download(url, id) {
          window.open(this.baseUrl + url, '_blank')

          this.$axios.get('addFileDownloadCount', {
              params: {
                  id: id
              }
          })
          this.fileList.forEach((item, index) => {
            if (item.id == id) {
                item.downloadCount += 1
                return true
            }
          })
      }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
