<template>
    <div>
        <!-- answer card -->
        <a-modal
            title="答题卡"
            v-model="visibleAnswerCard"
            @ok="submit"
            okText="交卷"
            cancelText="取消"
        >
            <h4>单选-A</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.singleA"
                        :key="index"
                        :class="question.answer ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>单选-B</h4>
            <h4>多选</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.multiple"
                        :key="index"
                        :class="question.answer.length != 0 ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>判断</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.judge"
                        :key="index"
                        class="answer-finished"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>填空</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.blank"
                        :key="index"
                        :class="question.answer.length != 0 && question.answer.filter((ans) => { return !!ans }).length == question.answer.length ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>问答</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.qa"
                        :key="index"
                        :class="question.answer ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
        </a-modal>
        <!-- navbar -->
        <navbar :userBaseInfo="userBaseInfo" />
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>开始刷题</h1>
                            <p class="subheading">(￣_,￣ )</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- anchor 
        <a-anchor :offsetTop="50" class="anchor">
            <a-anchor-link v-for="index in questions.singleA.length" :key="index" :href="'#' + (index-1)" :title="'第' + index + '题'" />
        </a-anchor> -->
        <!-- float card -->
        <div class="floatcard text-center">
            <h4>剩余时间</h4>
            <a-progress 
                type="circle"
                :percent="totalSeconds == -1 ? 100 : ((timer.hours()*3600+timer.minutes()*60+timer.seconds()) / totalSeconds).toFixed(4) * 100"
            >
            </a-progress>
            <p class="timer">
                {{ totalSeconds == -1 ? '无限制' : timer.hours() + 'h ' + timer.minutes() + 'm ' + timer.seconds() + 's' }}
            </p>
            <a-button v-if="totalSeconds != -1" type="primary">暂停</a-button>
        </div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <a-spin :spinning="loading">
                        <a-tabs defaultActiveKey="1">
                            <!-- singleA -->
                            <a-tab-pane tab="单选-A" key="singleA">
                                <span class="summary">共选取 {{ questions.singleA.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.singleA"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title }}</h4>
                                            </a-list-item-meta>
                                            <a-radio-group v-model="item.answer" buttonStyle="solid">
                                                <a-radio-button value="A">A. {{ item.A }}</a-radio-button>
                                                <a-radio-button value="B">B. {{ item.B }}</a-radio-button>
                                                <a-radio-button value="C">C. {{ item.C }}</a-radio-button>
                                                <a-radio-button value="D">D. {{ item.D }}</a-radio-button>
                                                <a-radio-button v-if="item.E" value="E">E. {{ item.E }}</a-radio-button>
                                            </a-radio-group>
                                        </div>
                                    </a-list-item>
                                </a-list>
                            </a-tab-pane>
                            <!-- singleB -->
                            <a-tab-pane tab="单选-B" key="singleB">
                                
                            </a-tab-pane>
                            <!-- multiple -->
                            <a-tab-pane tab="多选" key="multiple">
                                <span class="summary">共选取 {{ questions.multiple.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.multiple"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title }}</h4>
                                            </a-list-item-meta>
                                            <a-checkbox-group v-model="item.answer">
                                                <a-checkbox value="A">A. {{ item.A }}</a-checkbox>
                                                <a-checkbox value="B">A. {{ item.B }}</a-checkbox>
                                                <a-checkbox value="C">A. {{ item.C }}</a-checkbox>
                                                <a-checkbox value="D">A. {{ item.D }}</a-checkbox>
                                                <a-checkbox v-if="item.E" value="E">E. {{ item.E }}</a-checkbox>
                                            </a-checkbox-group>
                                        </div>
                                    </a-list-item>
                                </a-list>
                            </a-tab-pane>
                            <!-- blank -->
                            <a-tab-pane tab="填空" key="blank">
                                <span class="summary">共选取 {{ questions.blank.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.blank"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title }}</h4>
                                            </a-list-item-meta>
                                            <a-input
                                                v-for="title, index in parseBlanks(item.title)"
                                                :key="index"
                                                :placeholder="title"
                                                @change="changeBlank($event, item, index)"
                                            >
                                                <a-icon slot="prefix" type="question" />
                                            </a-input>
                                        </div>
                                    </a-list-item>
                                </a-list>
                            </a-tab-pane>
                            <!-- judge -->
                            <a-tab-pane tab="判断" key="judge">
                                <span class="summary">共选取 {{ questions.judge.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.judge"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title }}</h4>
                                            </a-list-item-meta>
                                            <a-switch v-model="item.answer">
                                                <a-icon type="check" slot="checkedChildren"/>
                                                <a-icon type="close" slot="unCheckedChildren"/>
                                            </a-switch>
                                        </div>
                                    </a-list-item>
                                </a-list>
                            </a-tab-pane>
                            <!-- qa -->
                            <a-tab-pane tab="问答" key="qa">
                                <span class="summary">共选取 {{ questions.qa.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.qa"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title }}</h4>
                                            </a-list-item-meta>
                                            <a-textarea 
                                                v-model="item.answer"
                                                placeholder="输入您的答案(注意：问答题系统不会进行核验，请对照答案自行校对)"
                                                :rows="4"
                                            />
                                        </div>
                                    </a-list-item>
                                </a-list>
                            </a-tab-pane>
                        </a-tabs>
                    </a-spin>
                    <a-button type="primary" style="width: 100%; margin-top: 50px;" @click="visibleAnswerCard = true">交卷</a-button>
                </div>
            </div>
        </div>

        <Footer />

        <a-back-top />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        loading: true,
        visibleAnswerCard: false,
        timerInterval: null,
        totalSeconds: 0
    }
  },
  async asyncData({ $axios, store, redirect }) {
    let userBaseInfo = null
    let questions = JSON.parse(JSON.stringify(store.state.bank.questions))
    let timer = moment.duration(store.state.bank.timer)

    // modify the type of questions_blank's answer
    questions.blank.forEach((blank) => {
        blank.answer = new Array()
    })
    // modify the type of questions_multiple's answer
    questions.multiple.forEach((multiple) => {
        multiple.answer = new Array()
    })
    // modify the type of questions_judge's answer
    questions.judge.forEach((judge) => {
        judge.answer = false
    })

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
        if (userBaseInfo.uid == -1) {
            redirect({ path: '/' })
        }
    })

    return {
        userBaseInfo: userBaseInfo,
        questions: questions,
        timer: timer,
        totalSeconds: timer.hours() * 3600 + timer.minutes() * 60 + timer.seconds()
    }
  },
  methods: {
      parseBlanks(blanks) {
          let regex = new RegExp(/{(.)}/, 'g')
          let result = []
          let array = []
          while ((array = regex.exec(blanks))) {
              result.push(array[1])
          }
          return result
      },
      changeBlank(e, item, index) {
          this.$set(item.answer, index, e.target.value)
      },
      submit() {
          this.$confirm({
              title: '确认',
              content: '确定交卷？',
              onOk: () => {
                  this.$axios.post('handExam', JSON.stringify({
                      singleA: this.questions.singleA,
                      singleB: this.questions.singleB,
                      multiple: this.questions.multiple,
                      judge: this.questions.judge,
                      blank: this.questions.blank,
                      qa: this.questions.qa
                  }))
                  .then((response) => {

                  })
              }
          })
      }
  },
  mounted() {
      clearInterval(this.timerInterval)
      this.timerInterval = setInterval(() => {
          if (this.timer.hours() == 0 && this.timer.minutes() == 0 && this.timer.seconds() == 0) {
              this.totalSeconds = -1
          }
          else {
            this.timer.subtract(1, 's')
            if (this.timer.hours() == 0 && this.timer.minutes() == 0 && this.timer.seconds() == 0) {
                clearInterval(this.timerInterval)
                this.$message.warning('kkk')
            }
          }
      }, 1000)
      this.loading = false
  },
  destroyed() {
      clearInterval(this.timerInterval)
  }
}
</script>

<style scoped>
.floatcard {
    float: right;
    position: fixed;
    right: 60px;
    top: 200px;
}
.floatcard h4 {
    color: red;
}

.timer {
    color: red;
    font-weight: bold;
    font-size: 24px;
}

.answer-finished {
    background-color: greenyellow;
}
.answer-unfinished {
    background-color: red;
}

.anchor {
    float: left;
    margin-left: 60px;
    width: 200px;
}
.anchor >>> .ant-anchor-link-title {
    text-decoration: none;
}

.summary {
    color: red;
    font-weight: bold;
}
</style>
