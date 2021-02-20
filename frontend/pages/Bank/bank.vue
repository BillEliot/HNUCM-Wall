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
                        @click="jumpTo('singleA', `singleA_${index}`)"
                        :class="question.answer ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>单选-B</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.singleB"
                        :key="index"
                        @click="jumpTo('singleB', `singleB_${index}`)"
                        :class="question.answer.length != 0 && question.answer.filter(ans => { return !!ans }).length == question.answer.length ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>多选</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.multiple"
                        :key="index"
                        @click="jumpTo('multiple', `multiple_${index}`)"
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
                        @click="jumpTo('judge', `judge_${index}`)"
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
                        @click="jumpTo('blank', `blank_${index}`)"
                        :class="question.answer.length != 0 && question.answer.filter(ans => { return !!ans }).length == question.answer.length ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>名词解释</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.term"
                        :key="index"
                        @click="jumpTo('term', `term_${index}`)"
                        :class="question.answer ? 'answer-finished' : 'answer-unfinished'"
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
                        @click="jumpTo('qa', `qa_${index}`)"
                        :class="question.answer ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
            <h4>病案分析</h4>
            <div class="row">
                <div class="com-md-1 text-center">
                    <a-button
                        v-for="question,index in questions.case"
                        :key="index"
                        @click="jumpTo('case', `case_${index}`)"
                        :class="question.answer ? 'answer-finished' : 'answer-unfinished'"
                    >
                        {{ index+1 }}
                    </a-button>
                </div>
            </div>
        </a-modal>
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
        <div v-show="isFloatCardFixed" class="float-card-fixed text-center">
            <h4>剩余时间</h4>
            <a-progress 
                type="circle"
                :percent="totalSeconds == -1 ? 100 : Number(((timer.hours() * 3600 + timer.minutes() * 60 + timer.seconds()) / totalSeconds * 100).toFixed(2))"
            >
            </a-progress>
            <p class="timer">
                {{ totalSeconds == -1 ? '无限制' : timer.hours() + 'h ' + timer.minutes() + 'm ' + timer.seconds() + 's' }}
            </p>
            <a-button v-if="totalSeconds != -1" type="primary" @click="pause">暂停</a-button>
            <br />
            <a-checkbox v-model="isFloatCardFixed" style="margin-top: 10px">固定</a-checkbox>
        </div>
        <div v-show="!isFloatCardFixed" class="float-card text-center">
            <strong style="font-weight: bold">
                <span id="float-card">剩余时间</span>
            </strong>
            <div class="float-card-content" style="display: block">
                <a-progress 
                    type="circle"
                    :percent="totalSeconds == -1 ? 100 : Number(((timer.hours() * 3600 + timer.minutes() * 60 + timer.seconds()) / totalSeconds * 100).toFixed(2))"
                >
                </a-progress>
                <p class="timer">
                    {{ totalSeconds == -1 ? '无限制' : timer.hours() + 'h ' + timer.minutes() + 'm ' + timer.seconds() + 's' }}
                </p>
                <a-button v-if="totalSeconds != -1" type="primary" @click="pause">暂停</a-button>
                <br />
                <a-checkbox v-model="isFloatCardFixed" style="margin-top: 10px">固定</a-checkbox>
            </div>
        </div>

        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <a-spin :spinning="loading">
                        <a-tabs v-model="activeTab">
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
                                        <div :id="`singleA_${index}`" :tabindex="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title + '()' }}</h4>
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
                                <span class="summary">共选取 {{ questions.singleB.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.singleB"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="`singleB_${index}`" :tabindex="index">
                                            <div
                                                v-for="title, _index in parseSingleB(item.title)"
                                                :key="_index"
                                            >
                                                <a-list-item-meta>
                                                    <h4 slot="title">{{ (index+1) + '、 ' + title + '()' }}</h4>
                                                </a-list-item-meta>
                                                <a-radio-group @change="changeSingleB($event, item, _index)" buttonStyle="solid">
                                                    <a-radio-button value="A">A. {{ item.A }}</a-radio-button>
                                                    <a-radio-button value="B">B. {{ item.B }}</a-radio-button>
                                                    <a-radio-button value="C">C. {{ item.C }}</a-radio-button>
                                                    <a-radio-button value="D">D. {{ item.D }}</a-radio-button>
                                                    <a-radio-button v-if="item.E" value="E">E. {{ item.E }}</a-radio-button>
                                                </a-radio-group>
                                            </div>
                                        </div>
                                    </a-list-item>
                                </a-list>
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
                                        <div :id="`multiple_${index}`" :tabindex="index">
                                            <a-list-item-meta>
                                                <h4 slot="title">{{ (index+1) + '、 ' + item.title + '()' }}</h4>
                                            </a-list-item-meta>
                                            <a-checkbox-group v-model="item.answer">
                                                <a-checkbox value="A">A. {{ item.A }}</a-checkbox>
                                                <a-checkbox value="B">B. {{ item.B }}</a-checkbox>
                                                <a-checkbox value="C">C. {{ item.C }}</a-checkbox>
                                                <a-checkbox value="D">D. {{ item.D }}</a-checkbox>
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
                                        <div :id="`blank_${index}`" :tabindex="index">
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
                                        <div :id="`judge_${index}`" :tabindex="index">
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
                            <!-- term -->
                            <a-tab-pane tab="名词解释" key="term">
                                <span class="summary">共选取 {{ questions.term.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.term"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="`term_${index}`" :tabindex="index">
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
                                        <div :id="`qa_${index}`" :tabindex="index">
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
                            <!-- case -->
                            <a-tab-pane tab="病案分析" key="case">
                                <span class="summary">共选取 {{ questions.case.length }} 道题目</span>
                                <a-list
                                    itemLayout="vertical"
                                    size="large"
                                    :pagination="null"
                                    :dataSource="questions.case"
                                >
                                    <div slot="footer">题目数据来于<b>HNUCM</b>练习册</div>
                                    <a-list-item slot="renderItem" slot-scope="item, index" key="item.id">
                                        <div :id="`case_${index}`" :tabindex="index">
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

        <a-back-top />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapMutations } from 'vuex'

window.onbeforeunload = function(event) {
    event.returnValue = "Will leave this page"
}

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  data() {
    return {
        activeTab: 'singleA',
        isFloatCardFixed: false,
        loading: true,
        visibleAnswerCard: false,
        timerInterval: null,
        totalSeconds: 0
    }
  },
  async asyncData({ $axios, store, redirect }) {
    let questions = JSON.parse(JSON.stringify(store.state.bank.questions))
    let subject = store.state.bank.currentSubject
    let timer = moment.duration(store.state.bank.timer)

    // modify the type of questions_blank's answer
    questions.blank.forEach((blank) => {
        let num = 0
        for (let i = 0; i < blank.title.length; i++) {
            if (blank.title[i] == '{') num ++
        }

        blank.answer = new Array(num).fill('')
    })
    // modify the type of questions_singleB's answer
    questions.singleB.forEach((singleB) => {
        let num = 0
        for (let i = 0; i < singleB.title.length; i++) {
            if (singleB.title[i] == ';') num ++
        }

        singleB.answer = new Array(num).fill('')
    })
    // modify the type of questions_multiple's answer
    questions.multiple.forEach((multiple) => {
        multiple.answer = new Array()
    })
    // modify the type of questions_judge's answer
    questions.judge.forEach((judge) => {
        judge.answer = false
    })

    return {
        questions: questions,
        subject: subject,
        timer: timer,
        totalSeconds: timer.hours() * 3600 + timer.minutes() * 60 + timer.seconds()
    }
  },
  methods: {
      ...mapMutations({
          setQuestions: 'bank/setQuestions'
      }),

      parseBlanks(blanks) {
          let regex = new RegExp(/{()}/, 'g')
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
      parseSingleB(singleB) {
          return singleB.split(';')
      },
      changeSingleB(e, item, index) {
          this.$set(item.answer, index, e.target.value)
      },
      pause() {
          clearInterval(this.timerInterval)
          this.$confirm({
              title: '暂停',
              content: '点击继续答题',
              onOk: () => {
                  this.startTimer()
              },
              onCancel: () => {
                  this.startTimer()
              },
          })
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
                      term: this.questions.term,
                      qa: this.questions.qa,
                      case: this.questions.case,
                      subject: this.subject
                  }))
                  .then((response) => {
                      if (response.data.code == 200 && response.data.status == 'success') {
                          this.setQuestions(response.data.data)
                          this.$router.push({ path: '/bank/result' })
                      }
                  })
              }
          })
      },
      startTimer() {
          clearInterval(this.timerInterval)
          this.timerInterval = setInterval(() => {
              if (this.timer.hours() == 0 && this.timer.minutes() == 0 && this.timer.seconds() == 0) {
                  this.totalSeconds = -1
              }
              else {
                  this.timer.subtract(1, 's')
                  // time up
                  if (this.timer.hours() == 0 && this.timer.minutes() == 0 && this.timer.seconds() == 0) {
                      clearInterval(this.timerInterval)
                      this.$message.warning('时间到了')
                      this.$axios.post('handExam', JSON.stringify({
                          singleA: this.questions.singleA,
                          singleB: this.questions.singleB,
                          multiple: this.questions.multiple,
                          judge: this.questions.judge,
                          blank: this.questions.blank,
                          term: this.questions.term,
                          qa: this.questions.qa,
                          case: this.questions.case,
                  }))
                  .then((response) => {
                      this.setQuestions(response.data)
                      this.$router.push({ path: '/bank/result' })
                  })
                }
            }
        }, 1000)
      },
      jumpTo(type, id) {
          this.visibleAnswerCard = false
          this.activeTab = type
          setTimeout(() => {
              let offsetTop = document.getElementById(id).offsetTop
              window.scrollTo(0, offsetTop + 500)
          }, 1)
      }
  },
  mounted() {
      this.startTimer()
      this.loading = false
  },
  destroyed() {
      clearInterval(this.timerInterval)
  }
}
</script>

<style scoped>
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

.float-card-fixed {
    float: right;
    position: fixed;
    right: 60px;
    top: 200px;
    z-index: 9999;
}
.float-card-fixed h4 {
    color: red;
}

.float-card:hover {
    transition: '0.3s all ease-in';
    right: 0
}
.float-card-content {
    max-height: 260px;
    position: relative;
    overflow: auto;
}
span#float-card {
    position: absolute;
    left: -63px;
    -webkit-transform: rotate(90deg);
    transform: rotate(90deg);
    background: #ffc82c;
    width: auto;
    height: auto;
    top: 20px;
    padding: 7px 14px;
    border-radius: 15px;
    color: #123464;
    font-size: 18px;
}
.float-card {
    position: fixed;
    border: 1px solid #0099d6;
    border-radius: 10px;
    padding: 20px;
    display: inline-block;
    width: 200px;
    right: -200px;
    top: 30%;
    height: 260px;
    z-index: 9999;
    transition: right .35s ease-in-out;
}
</style>
