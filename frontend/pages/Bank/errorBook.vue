<template>
  <div>
    <!-- banner -->
    <div class="main-wrapper">
        <div class="page-title">
            <div class="container">
                <div class="title-holder">
                    <div class="title-text text-center">
                        <h1>错题本</h1>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div style="margin-top: 50px"></div>
    <!-- statement -->
    <section class="section">
      <div class="container">
        <a-tabs default-active-key="1">
          <a-tab-pane key="1" tab="错题">
            <a-popconfirm
              title="确定清空错题吗？"
              @confirm="confirm_clearErrorBook()"
              okText="是"
              cancelText="否"
            >
              <a-icon slot="icon" type="question-circle-o" style="color: red" />
              <a-button type="danger">清空错题</a-button>
            </a-popconfirm>
            <a-list
              v-if="errorBook.length"
              :pagination="errorBookPagination"
              :dataSource="errorBook"
              :header="`${errorBook.length} 个错题`"
              itemLayout="horizontal"
            >
              <div slot="footer"><b>做错的题目～</b></div>
              <a-list-item slot="renderItem" slot-scope="item">
                  <div>
                      <a-tag color="red">科目：{{ item.subject }}</a-tag>
                      <a-tag color="green">章节：{{ item.chapter }}</a-tag>
                      <h4 v-if="item.questionType == 'singleB'" v-for="title in parseSingleB(item.title)">
                        {{ title }}
                      </h4>
                      <h4 v-else>{{ item.title }}</h4>
                      <a-tag color="purple" v-if="item.A != ''">A. {{ item.A }}</a-tag>
                      <a-tag color="purple" v-if="item.B != ''">B. {{ item.B }}</a-tag>
                      <a-tag color="purple" v-if="item.C != ''">C. {{ item.C }}</a-tag>
                      <a-tag color="purple" v-if="item.D != ''">D. {{ item.D }}</a-tag>
                      <a-tag color="purple" v-if="item.E != ''">E. {{ item.E }}</a-tag>
                      <br />
                      <a-collapse :bordered="false">
                          <a-collapse-panel header="正确答案">
                              <p>{{ item.answer }}</p>
                          </a-collapse-panel>
                      </a-collapse>
                      <a-popconfirm
                          title="确定从错题本中删除这道题目吗？"
                          @confirm="confirm_removeErrorBook(item.id)"
                          okText="是"
                          cancelText="否"
                      >
                          <a-icon slot="icon" type="question-circle-o" style="color: red" />
                          <a-button type="danger" size="small" style="margin-top: 10px">删除题目</a-button>
                      </a-popconfirm>
                  </div>
              </a-list-item>
            </a-list>
          </a-tab-pane>
          <a-tab-pane key="2" tab="试卷">
            <a-popconfirm
              title="确定清空试卷吗？"
              @confirm="confirm_clearBankResult()"
              okText="是"
              cancelText="否"
            >
              <a-icon slot="icon" type="question-circle-o" style="color: red" />
              <a-button type="danger">清空试卷</a-button>
            </a-popconfirm>
            <a-table :columns="columns" :dataSource="bankResult" rowKey="id">
              <template slot="correctRate" slot-scope="text, record">
                {{ (record.correctQuestions / record.allQuestions * 100).toFixed(2) + '%' }}
              </template>
              <template slot="date" slot-scope="text">
                {{ moment(text).format('lll') }}
              </template>
              <span slot="action" slot-scope="text, record">
                <a @click="detailResult(record.json_serialization)">
                  详细
                </a>
                <a-divider type="vertical" />
                <a-popconfirm
                  title="确定删除吗？"
                  ok-text="确定"
                  cancel-text="取消"
                  @confirm="confirm_removeResult(record.id)"
                >
                  <a>删除</a>
                </a-popconfirm>
              </span>
            </a-table>
          </a-tab-pane>
        </a-tabs>
      </div>
    </section>
  </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState, mapMutations } from 'vuex'

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  data() {
    return {
      moment,

      errorBookPagination: {
        current: 1,
        pageSize: 10,
        onChange (page) {
          this.current = page
        }
      },
      columns: [{
        dataIndex: 'subject',
        title: '科目',
      }, {
        dataIndex: 'correctQuestions',
        title: '正确题目'
      }, {
        dataIndex: 'allQuestions',
        title: '全部题目',
      }, {
        title: '正确率',
        scopedSlots: { customRender: 'correctRate' }
      }, {
        dataIndex: 'date',
        title: '日期',
        scopedSlots: { customRender: 'date' }
      }, {
        title: '操作',
        scopedSlots: { customRender: 'action' }
      }]
    }
  },
  async asyncData({ $axios, app }) {
    let errorBook = []
    let bankResult = []

    await $axios.get('getErrorBook')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        errorBook = response.data.data
      }
    })
    await $axios.get('getBankResult')
    .then((response) => {
      if (response.data.code == 200 && response.data.status == 'success') {
        bankResult = response.data.data
      }
    })

    return {
      errorBook: errorBook,
      bankResult: bankResult
    }
  },
  methods: {
    ...mapMutations({
        setQuestions: 'bank/setQuestions'
    }),
    parseSingleB(singleB) {
        return singleB.split(';')
    },
    confirm_removeErrorBook(id) {
      this.$axios.get('removeErrorBook', {
        params: {
          id: id
        }
      })
      .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
          this.errorBook.forEach((item, index) => {
            if (item.id == id) {
              this.errorBook.splice(index, 1)
              this.$message.success('删除成功')
              return true
            }
          })
        }
      })
    },
    confirm_clearErrorBook() {
      if (this.errorBook.length == 0) {
        this.$message.warning('错题本已经是空的了～')
      }
      else {
        this.$axios.get('clearErrorBook')
        .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
            this.errorBook = []
            this.$message.success('清除成功')
          }
        })
      }
    },
    detailResult(json_serialization) {
      this.setQuestions(JSON.parse(json_serialization))
      this.$router.push({ path: '/bank/result', query: { isResult: true } })
    },
    confirm_removeResult(id) {
      this.$axios.get('removeBankResult', {
        params: {
          id: id
        }
      })
      .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
          this.bankResult.forEach((item, index) => {
            if (item.id == id) {
              this.bankResult.splice(index, 1)
              this.$message.success('删除成功')
              return true
            }
          })
        }
      })
    },
    confirm_clearBankResult() {
      if (this.bankResult.length == 0) {
        this.$message.warning('错题本已经是空的了～')
      }
      else {
        this.$axios.get('clearBankResult')
        .then((response) => {
          if (response.data.code == 200 && response.data.status == 'success') {
            this.bankResult = []
            this.$message.success('清除成功')
          }
        })
      }
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
