<template>
    <div>
        <!-- navbar -->
        <navbar :userBaseInfo="userBaseInfo" />
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>答题结果</h1>
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
                                                <h4 slot="title" :class="item.isCorrect ? 'correct' : 'uncorrect'">
                                                    {{ (index+1) + '、 ' + item.title + ' (' + item.bank + ')' }}
                                                </h4>
                                            </a-list-item-meta>
                                            <a-radio-group v-model="item.answer" buttonStyle="solid" disabled>
                                                <a-radio-button value="A">A. {{ item.A }}</a-radio-button>
                                                <a-radio-button value="B">B. {{ item.B }}</a-radio-button>
                                                <a-radio-button value="C">C. {{ item.C }}</a-radio-button>
                                                <a-radio-button value="D">D. {{ item.D }}</a-radio-button>
                                                <a-radio-button v-if="item.E" value="E">E. {{ item.E }}</a-radio-button>
                                            </a-radio-group>
                                            <div v-if="!item.isCorrect" class="fault-action">
                                                <h4>正确答案：{{ item.correctAnswer }}</h4>
                                                <a-button type="primary">加入错题本</a-button>
                                            </div>
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
                                                <h4 slot="title" :class="item.isCorrect ? 'correct' : 'uncorrect'">
                                                    {{ (index+1) + '、 ' + item.title + ' (' + item.bank + ')' }}
                                                </h4>
                                            </a-list-item-meta>
                                            <a-checkbox-group v-model="item.answer" disabled>
                                                <a-checkbox value="A">A. {{ item.A }}</a-checkbox>
                                                <a-checkbox value="B">A. {{ item.B }}</a-checkbox>
                                                <a-checkbox value="C">A. {{ item.C }}</a-checkbox>
                                                <a-checkbox value="D">A. {{ item.D }}</a-checkbox>
                                                <a-checkbox v-if="item.E" value="E">E. {{ item.E }}</a-checkbox>
                                            </a-checkbox-group>
                                            <div v-if="!item.isCorrect" class="fault-action">
                                                <h4>正确答案：{{ item.correctAnswer }}</h4>
                                                <a-button type="primary">加入错题本</a-button>
                                            </div>
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
                                                <h4 slot="title" :class="item.isCorrect ? 'correct' : 'uncorrect'">
                                                    {{ (index+1) + '、 ' + item.title + ' (' + item.bank + ')' }}
                                                </h4>
                                            </a-list-item-meta>
                                            <a-input
                                                v-for="title, index in parseBlanks(item.title)"
                                                :key="index"
                                                :placeholder="item.answer[index]"
                                                disabled
                                            >
                                                <a-icon slot="prefix" type="question" />
                                            </a-input>
                                            <div v-if="!item.isCorrect" class="fault-action">
                                                <h4>正确答案：{{ item.correctAnswer }}</h4>
                                                <a-button type="primary">加入错题本</a-button>
                                            </div>
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
                                                <h4 slot="title" :class="item.isCorrect ? 'correct' : 'uncorrect'">
                                                    {{ (index+1) + '、 ' + item.title + ' (' + item.bank + ')' }}
                                                </h4>
                                            </a-list-item-meta>
                                            <a-switch v-model="item.answer" disabled>
                                                <a-icon type="check" slot="checkedChildren"/>
                                                <a-icon type="close" slot="unCheckedChildren"/>
                                            </a-switch>
                                            <div v-if="!item.isCorrect" class="fault-action">
                                                <h4>正确答案：{{ item.correctAnswer ? '正确' : '错误' }}</h4>
                                                <a-button type="primary">加入错题本</a-button>
                                            </div>
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
                                                <h4 slot="title">
                                                    {{ (index+1) + '、 ' + item.title + ' (' + item.bank + ')' }}
                                                </h4>
                                            </a-list-item-meta>
                                            <a-textarea
                                                v-model="item.answer"
                                                placeholder="输入您的答案(注意：问答题系统不会进行核验，请对照答案自行校对)"
                                                :rows="4"
                                                disabled
                                            />
                                        </div>
                                    </a-list-item>
                                </a-list>
                            </a-tab-pane>
                        </a-tabs>
                    </a-spin>
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
import { mapMutations } from 'vuex'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        loading: true
    }
  },
  async asyncData({ $axios, store, redirect }) {
    let userBaseInfo = null
    let questions = JSON.parse(JSON.stringify(store.state.bank.questions))

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
        if (userBaseInfo.uid == -1) {
            redirect({ path: '/' })
        }
    })

    return {
        userBaseInfo: userBaseInfo,
        questions: questions
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
      }
  },
  mounted() {
      this.loading = false
  }
}
</script>

<style scoped>
.correct {
    color: green;
}
.uncorrect {
    color: red;
}

.fault-action {
    margin-top: 30px;
    color: green;
    font-weight: bold;
}

.summary {
    color: red;
    font-weight: bold;
}
</style>
