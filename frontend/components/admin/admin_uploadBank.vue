<template>
    <div>
        <div class="container">
            <div class="title-holder">
                <div class="title-text text-center">
                    <h1>导入题库</h1>
                    <span class="subheading">请导入csv类型的题库</span><br />
                    <span class="field">title</span><br />
                    <span class="field">A</span><br />
                    <span class="field">B</span><br />
                    <span class="field">C</span><br />
                    <span class="field">D</span><br />
                    <span class="field">E</span><br />
                    <span class="field">questionType(singleA;singleB;multiple;blank;judge;term;qa;case)</span><br />
                    <span class="field">isBlankSeq(1;0)</span><br />
                    <span class="field">answer</span><br />
                </div>
            </div>
        </div>
        <hr />
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <a-select v-model="subject" class="col-md-3">
                        <a-select-opt-group>
                            <span slot="label"><a-icon type="heat-map"/>中医类</span>
                            <a-select-option v-for="subject in zySubjects" :key="subject" :value="subject">{{ subject }}</a-select-option>
                        </a-select-opt-group>
                        <a-select-opt-group>
                            <span slot="label"><a-icon type="stock"/>西医类</span>
                            <a-select-option v-for="subject in xySubjects" :key="subject" :value="subject">{{ subject }}</a-select-option>
                        </a-select-opt-group>
                    </a-select>
                    <a-select v-model="chapter" class="col-md-3">
                        <a-select-option v-for="chp in chapters" :key="chp">
                            {{ chp }}
                        </a-select-option>
                    </a-select>
                    <a-input v-model="comment" class="col-md-3" placeholder="请输入备注" />
                    <a-upload
                        name="uploadBank"
                        accept=".csv"
                        :multiple="false"
                        :action="baseUrl + '/api/uploadBank'"
                        :data="{
                            subject: this.subject,
                            chapter: this.chapter,
                            comment: this.comment,
                        }"
                        supportServerRender
                        :beforeUpload="beforeUpload"
                        @change="handleChange"
                        class="col-md-3"
                    >
                        <a-button>
                            <a-icon type="upload" /> 上传
                        </a-button>
                    </a-upload>
                    <hr />
                    <a-list item-layout="horizontal" :data-source="bankUploadHistory" :pagination="pagination" class="col-md-12">
                        <a-list-item slot="renderItem" slot-scope="item, index">
                            <a-list-item-meta
                                :description="item.comment + ' ' + item.date"
                            >
                                <router-link slot="title" :to="{ path: '/profile', query: { id: item.user.id } }">{{ item.user.username }}</router-link>
                                <a-avatar
                                    slot="avatar"
                                    :src="baseUrl + item.user.avatar"
                                />
                            </a-list-item-meta>
                        </a-list-item>
                    </a-list>
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
  props: ['userBaseInfo', 'zySubjects', 'xySubjects', 'bankUploadHistory'],
  data() {
    return {
        comment: '',
        subject: '选择科目',
        chapters: [],
        chapter: '选择章节',
        pagination: {
            current: 1,
            pageSize: 10,
            onChange (page) {
                this.current = page
            }
        },
    }
  },
  methods: {
      beforeUpload(file, filelist) {
          if (this.subject == '' || this.chapter == '' || this.comment == '' || this.subject == '选择科目' || this.chapter == '选择章节') {
              this.$message.warning('请填写完整信息')
              this.$message.info(`${info.file.name} 停止上传`)
              return false
          }
          filelist = []
          return true
      },
      handleChange(info) {
          if (info.file.status !== 'uploading') {
              this.$message.info(`${info.file.name} 正在上传`)
          }
          if (info.file.status === 'done') {
              this.$message.success(`${info.file.name} 上传成功`)
              this.bankUploadHistory.unshift({
                  comment: info.file.name + '/' + this.comment,
                  user: { username: this.userBaseInfo.username, avatar: this.userBaseInfo.avatar },
                  date: moment().format("YYYY-MM-DD")
              })
          } else if (info.file.status === 'error') {
              this.$message.error(`${info.file.name} 上传失败`)
          }
      }
  },
  computed: mapState({
    baseUrl: state => state.baseUrl
  }),
  watch: {
      subject(val) {
          this.chapter = ''
          this.$axios.get('getBankChapters', {
              params: {
                  subject: val
              }
          })
          .then((response) => {
              this.chapters = response.data.info
          })
      }
  }
}
</script>

<style scoped>
a {
    text-decoration: none;
}

.subheading {
    color: red;
    font-weight: bold;
}

.field {
    color: green;
    font-weight: bold;
}
</style>
