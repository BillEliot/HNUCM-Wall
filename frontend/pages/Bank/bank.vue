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
                            <h1>开始刷题</h1>
                            <p class="subheading">(￣_,￣ )</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- anchor -->
        <a-anchor :offsetTop="50" class="anchor">
            <a-anchor-link v-for="index in questions.length" :key="index" :href="'#' + (index-1)" :title="'第' + index + '题'" />
        </a-anchor>
        <!-- float card -->
        <div class="floatcard text-center">
            <h4>已用时</h4>
            <a-progress type="circle" :percent="75" />
            <h4>剩余时间</h4>
            <a-progress type="circle" :percent="75" />
        </div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <span class="summary">共选取 {{ questions.length }} 道题目</span>
                    <a-list
                        itemLayout="vertical"
                        size="large"
                        :pagination="pagination"
                        :dataSource="questions"
                    >
                        <div slot="footer">powered by <b>HNUCM-wall</b></div>
                        <a-list-item slot="renderItem" slot-scope="item, index" key="item.title">
                            <div :id="index">
                                <a-list-item-meta>
                                    <h4 slot="title">{{ item.title }}</h4>
                                </a-list-item-meta>
                                <!-- singleA -->
                                <div v-if="item.questionType == 'singleA'">
                                    <a-radio-group defaultValue="A" buttonStyle="solid">
                                        <a-radio-button value="A">A. {{ item.A }}</a-radio-button>
                                        <a-radio-button value="B">B. {{ item.B }}</a-radio-button>
                                        <a-radio-button value="C">C. {{ item.C }}</a-radio-button>
                                        <a-radio-button value="D">D. {{ item.D }}</a-radio-button>
                                        <a-radio-button v-if="item.E" value="E">E. {{ item.E }}</a-radio-button>
                                    </a-radio-group>
                                </div>
                                <!-- multiple -->
                                <div v-else-if="item.questionType == 'multiple'">
                                    <a-checkbox-group>
                                        <a-checkbox value="A">A. {{ item.A }}</a-checkbox>
                                        <a-checkbox value="B">A. {{ item.B }}</a-checkbox>
                                        <a-checkbox value="C">A. {{ item.C }}</a-checkbox>
                                        <a-checkbox value="D">A. {{ item.D }}</a-checkbox>
                                        <a-checkbox v-if="item.E" value="E">E. {{ item.E }}</a-checkbox>
                                    </a-checkbox-group>
                                </div>
                                <!-- blank -->
                                <div v-else-if="item.questionType == 'blank'">
                                    <a-input v-for="index in parseBlanks(item.title)" :key="index" :placeholder="index" >
                                        <a-icon slot="prefix" type="question" />
                                    </a-input>
                                </div>
                                <!-- judge -->
                                <div v-else-if="item.questionType == 'judge'">
                                    <a-switch >
                                        <a-icon type="check" slot="checkedChildren"/>
                                        <a-icon type="close" slot="unCheckedChildren"/>
                                    </a-switch>
                                </div>
                                <!-- judge -->
                                <div v-else-if="item.questionType == 'qa'">
                                    <a-textarea placeholder="输入您的答案(注意：问答题系统不会进行核验，请对照答案自行校对)" :rows="4"/>
                                </div>
                            </div>
                        </a-list-item>
                    </a-list>
                    <a-button type="primary" style="width: 100%; margin-top: 50px;">交卷</a-button>
                </div>
            </div>
        </div>

        <Footer />

        <a-back-top />

    </div>
</template>

<script>
import qs from 'qs'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        pagination: {
            current: 1,
            onChange(page) {
                current = page
            },
            pageSize: 10
        }
    }
  },
  async asyncData({ $axios, store, redirect }) {
    let userBaseInfo = null
    let questions = store.state.bank.questions
    let timer = store.state.bank.timer

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
        timer: timer
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
  }
}
</script>

<style scoped>
.anchor {
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
