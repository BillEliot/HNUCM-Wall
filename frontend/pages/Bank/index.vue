<template>
    <div>
        <a-drawer
            title="题库更新"
            placement="right"
            :closable="false"
            :visible="visible_update"
            @close="visible_update = false"
        >
            <a-timeline>
                <a-timeline-item v-for="message in bankUpdateMessage" :key="message">{{ message }}</a-timeline-item>
            </a-timeline>
        </a-drawer>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>题库</h1>
                            <p class="subheading">伟大的题库</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="text-center">
                <div class="row">
                    <div class="col-md-4 col-xs-12 col-sm-4 cellwarpper">
                        <a-icon type="radar-chart" style="font-size: 128px" />
                        <div class="cell">
                            <h2>全面</h2>
                        </div>
                    </div>
                    <div class="col-md-4 col-xs-12 col-sm-4 cellwarpper">
                        <a-icon type="area-chart" style="font-size: 128px" />
                        <div class="cell">
                            <h2>效率</h2>
                        </div>
                    </div>
                    <div class="col-md-4 col-xs-12 col-sm-4 cellwarpper">
                        <a-icon type="pie-chart" style="font-size: 128px" />
                        <div class="cell">
                            <h2>便捷</h2>
                        </div>
                    </div>
                </div>
                <hr />
                <div class="row">
                    <div class="col-md-4 col-xs-12 col-sm-4 cellwarpper">
                        <a-icon type="bar-chart" style="font-size: 128px" />
                        <div class="cell">
                            <h2>发现</h2>
                        </div>
                    </div>
                    <div class="col-md-4 col-xs-12 col-sm-4 cellwarpper">
                        <a-icon type="rise" style="font-size: 128px" />
                        <div class="cell">
                            <h2>提升</h2>
                        </div>
                    </div>
                    <div class="col-md-4 col-xs-12 col-sm-4 cellwarpper">
                        <a-icon type="dot-chart" style="font-size: 128px" />
                        <div class="cell">
                            <h2>自信</h2>
                        </div>
                    </div>
                </div>
                <hr />
            </div>
            <!-- Main -->
            <h1 class="title">开始刷题吧</h1>
            <div class="text-left">
                <div class="text-center notice">
                    <span>题库数据来源于练习册及网络</span>
                    <br />
                    <span>推荐使用PC端以获得最佳体验</span>
                    <br />
                    <a-button type="link" size="small" @click="visible_update = true">查看更新</a-button>
                </div>
                <a-form :form="form_bank" @submit="submitBank">
                    <a-form-item v-bind="formItemLayout">
                        <span slot="label">
                            刷题策略&nbsp;
                            <a-tooltip title="初期你可以刷全部题库，后期可以选择随机组题来检验自己">
                                <a-icon type="question-circle-o" />
                            </a-tooltip>
                        </span>
                        <a-radio-group
                            v-decorator="[
                                'type',
                                {
                                    initialValue: 'total'
                                }
                            ]"
                            buttonStyle="solid"
                        >
                            <a-radio-button value="total" @click="selectAllBank">全部题库</a-radio-button>
                            <a-radio-button value="random" @click="selectRandomBank">随机组题</a-radio-button>
                        </a-radio-group>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout" label="选择题库">
                        <a-select
                            v-decorator="[
                                'banks', {
                                    rules: [{ required: true, message: '请至少选择一个题库' }],
                                    getValueFromEvent: selectBank
                                }
                            ]"
                        >
                            <a-select-opt-group>
                                <span slot="label"><a-icon type="heat-map"/>中医类</span>
                                <a-select-option v-for="subject in zySubjects" :key="subject" :value="subject">{{ subject }}</a-select-option>
                            </a-select-opt-group>
                            <a-select-opt-group>
                                <span slot="label"><a-icon type="stock"/>西医类</span>
                                <a-select-option v-for="subject in xySubjects" :key="subject" :value="subject">{{ subject }}</a-select-option>
                            </a-select-opt-group>
                        </a-select>
                    </a-form-item>
                    
                    <a-form-item v-bind="formItemLayout" label="选择子章">
                        <a-tree
                            v-decorator="[
                                'selectChapters', {
                                    rules: [{ validator: validatorTransfer }]
                                }
                            ]"
                            checkable
                            show-line
                            :selectable="false"
                            :default-expanded-keys="['root']"
                            @check="selectChapter"
                            v-if="this.subject != '科目'"
                            class="select-chapter"
                        >
                            <a-tree-node key="root" :title="this.subject">
                                <a-tree-node v-if="hasTestPaper" key="testPaper">
                                    <span slot="title" style="color: #A52A2A">模拟试卷</span>
                                    <a-tree-node v-for="chapter, index in this.chapters" v-if="chapter.isTestPaper" :key="chapter.key">
                                        <a-icon slot="switcherIcon" type="carry-out" />
                                        <span slot="title" style="color: #FF8C00">{{ chapter.title }}</span>
                                    </a-tree-node>
                                </a-tree-node>
                                <a-tree-node v-for="chapter, index in this.chapters" v-if="!chapter.isTestPaper" :key="chapter.key">
                                    <span slot="title" style="color: #1890ff">{{ chapter.title }}</span>
                                </a-tree-node>
                            </a-tree-node>
                        </a-tree>
                    </a-form-item>
                    <a-form-item
                        v-bind="formItemLayout"
                        label="题目总数"
                        v-show="form_bank.getFieldValue('type') == 'random'"
                    >
                        <a-row :gutter="16">
                            <a-col :span="20">
                                <a-slider
                                    v-decorator="[
                                        'numQuestion',
                                        {
                                            initialValue: 0
                                        }
                                    ]"
                                    :min="1"
                                    :max="maxNumQuestion"
                                />
                            </a-col>
                            <a-col :span="4">
                                <span>{{ form_bank.getFieldValue('numQuestion') }} 道题目</span>
                            </a-col>
                        </a-row>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout">
                        <span slot="label">
                            题型占比&nbsp;
                            <a-tooltip title="当策略为【全部题库】时，题型占比为【该题型占所选题库该题型的百分比】；当策略为【随机组题】时，题型占比为【该题型占所有题型的百分比】">
                                <a-icon type="question-circle-o" />
                            </a-tooltip>
                        </span>
                        <a-form-item label="单选-A型题目" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'singleA',
                                    {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks" 
                            />
                        </a-form-item>
                        <a-form-item label="单选-B型题目" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'singleB',
                                    {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks" 
                            />
                        </a-form-item>
                        <a-form-item label="多选" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'multiple',
                                    {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks" 
                            />
                        </a-form-item>
                        <a-form-item label="填空" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'blank',
                                    {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks" 
                            />
                        </a-form-item>
                        <a-form-item label="判断" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'judge',
                                    {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks" 
                            />
                        </a-form-item>
                        <a-form-item label="名词解释" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'term', {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks"
                            />
                        </a-form-item>
                        <a-form-item label="问答" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'qa', {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks"
                            />
                        </a-form-item>
                        <a-form-item label="病案分析" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'case', {
                                        initialValue: 100
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks"
                            />
                        </a-form-item>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout">
                        <span slot="label">
                            设置时间限制&nbsp;
                            <a-tooltip title="你可以限制在一个时段内答题">
                                <a-icon type="question-circle-o" />
                            </a-tooltip>
                        </span>
                        <a-time-picker
                            v-decorator="[
                                'timer'
                            ]"
                            :minuteStep="15"
                            :secondStep="10"
                        />
                    </a-form-item>
                    <a-form-item v-bind="tailFormItemLayout">
                        <a-button type="primary" html-type="submit" style="width: 100%" >开始刷题</a-button>
                    </a-form-item>
                </a-form>
            </div>
        </div>

        <Footer />

    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState, mapGetters, mapActions } from 'vuex'


export default {
  layout: 'common',
  data() {
    return {
        form_bank: this.$form.createForm(this),
        subject: '科目',
        hasTestPaper: false,
        chapters: [],
        targetChapters: [],
        maxNumQuestion: 0,
        marks: {
            0: '0',
            16: '16%',
            50: '50%',
            100: '100%',
        },
        formItemLayout: {
            labelCol: {
                span: 6,
            },
            wrapperCol: {
                span: 12
            },
        },
        tailFormItemLayout: {
            wrapperCol: {
                md: {
                    span: 12,
                    offset: 6,
                },
                sm: {
                    span: 10,
                    offset: 6
                }
            }
        },
        visible_update: false,
        bankUpdateMessage: []
    }
  },
  async asyncData({ $axios, store }) {
    let bankUpdateMessage = []
    let zySubjects = []
    let xySubjects = []
    
    // Get subjects and chapters
    await $axios.get('getBankSubjects')
    .then((response) => {
        store.commit('bank/setSubjects', response.data.data)
        response.data.data.forEach(subject => {
            if (subject.subjectType == 'zy') {
                zySubjects.push(subject.key)
            }
            else if (subject.subjectType == 'xy') {
                xySubjects.push(subject.key)
            }
        })
    })

    await $axios.get('getBankUpdateMessage')
    .then((response) => {
        bankUpdateMessage = response.data.info
    })

    return {
        bankUpdateMessage: bankUpdateMessage,
        zySubjects: zySubjects,
        xySubjects: xySubjects
    }
  },
  methods: {
      ...mapActions({
          setBank: 'bank/setBank'
      }),

      validatorTransfer(rule, value, callback) {
          if (this.targetChapters.length == 0) {
              callback('请至少选择一个子章节')
          }
          callback()
      },
      selectAllBank() {
          this.form_bank.setFieldsValue({
              'singleA': 100,
              'singleB': 100,
              'multiple': 100,
              'blank': 100,
              'judge': 100,
              'term': 100,
              'qa': 100,
              'case': 100
          })
      },
      selectRandomBank() {
          this.form_bank.setFieldsValue({
              'singleA': 13,
              'singleB': 12,
              'multiple': 13,
              'blank': 12,
              'judge': 12,
              'term': 13,
              'qa': 13,
              'case': 12
          })
      },
      selectBank(value) {
          this.subject = value
          this.chapters = this.getChapters(value)
          let isHasTestPaper = this.chapters.some((chapter) => {
              return chapter.isTestPaper == true
          })
          if (isHasTestPaper) this.hasTestPaper = true
          else this.hasTestPaper = false

          this.form_bank.setFieldsValue({
              'numQuestion': 0
          })
          this.maxNumQuestion = 0
          return value
      },
      selectChapter(checkedKey) {
          this.targetChapters = []
          this.form_bank.setFieldsValue({
              'numQuestion': 0
          })
          this.maxNumQuestion = 0
          for (let i = checkedKey.length - 1; i>=0; i--) {
              if (checkedKey[i] != 'root' && checkedKey[i] != 'testPaper') {
                  this.targetChapters.push(checkedKey[i])
                  // get quantity of selected banks' question
                  this.$axios.get('getNumQuestion', {
                      params: {
                          subject: this.subject,
                          chapters: this.targetChapters
                      }
                  })
                  .then((response) => {
                      if (response.data.code == 200 && response.data.status == 'success') {
                          this.maxNumQuestion += response.data
                          this.form_bank.setFieldsValue({
                              'numQuestion': this.form_bank.getFieldValue('numQuestion') + response.data.data
                          })
                      }
                  })
              }
          }
      },
      chapterFilter(inputValue, option) {
          return option.title.indexOf(inputValue) > -1
      },
      submitBank(e) {
          e.preventDefault()
          this.form_bank.validateFields((err, values) => {
              if (!err) {
                  let { singleA,singleB,multiple,blank,judge,term,qa,_case } = this.form_bank.getFieldsValue(['singleA', 'singleB', 'multiple', 'blank', 'judge', 'term', 'qa', 'case'])
                  if (this.userBaseInfo.id == -1) {
                      this.$message.warning('先登录吧～')
                  }
                  else if (values.type == 'random' && singleA+singleB+multiple+blank+judge+term+qa+_case > 100) {
                      this.$message.warning('题型占比超过100%, 请检查')
                  }
                  else if (values.type == 'random' && singleA+singleB+multiple+blank+judge+term+qa+_case < 100) {
                      this.$message.warning('题型占比不足100%, 请检查')
                  }
                  else {
                      this.$axios.post('submitBank', qs.stringify({
                          type: values.type,
                          chapters: this.targetChapters,
                          numQuestion: this.form_bank.getFieldValue('numQuestion'),
                          singleA: values.singleA,
                          singleB: values.singleB,
                          multiple: values.multiple,
                          blank: values.blank,
                          judge: values.judge,
                          term: values.term,
                          qa: values.qa,
                          case: values.case
                      }, { arrayFormat: 'brackets' }))
                      .then((response) => {
                          if (response.data.code == 200 && response.data.status == 'success') {
                              this.setBank({ 
                                  'questions': response.data.data,
                                  'timer': moment.duration({
                                      seconds: values.timer ? values.timer.second() : 0,
                                      minutes: values.timer ? values.timer.minute() : 0,
                                      hours: values.timer ? values.timer.hour() : 0
                                  }),
                                  'subject': this.subject
                              })
                              this.$router.push({ path: '/bank/bank' })
                          }
                      })
                  }
              }
          })
      },
      rangeFormatter(value) {
          return `${value} %`
      }
  },
  computed: {
      ...mapState({
          banks: state => state.bank.banks,
          userBaseInfo: state => state.userBaseInfo
      }),
      ...mapGetters({
          getChapters: 'bank/getChapters'
      })
  }
}
</script>

<style scoped>
.notice {
    margin-bottom: 30px;
    font-weight: bold;
    color: red;
}

.cellwarpper {
    display: table;
}
.cell {
    display: table-cell;
    vertical-align: middle;
}

.title {
    margin-top: 30px;
    margin-bottom: 30px;
    color: green;
    text-align: center;
}

.questionPercent {
    margin-bottom: 0;
}
.questionPercent >>> .ant-slider {
    margin-top: 0
}

.select-chapter {
    height: 250px;
    overflow-y: scroll;
    overflow-x: hidden;
    border: solid 1px;
    border-radius: 10px;
    padding: 10px;
}
</style>
