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
                            <h1>题库</h1>
                            <p class="subheading">伟大的题库～</p>
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
            <h1 class="title">开始刷题吧～</h1>
            <div class="text-left">
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
                            <a-radio-button value="total">全部题库</a-radio-button>
                            <a-radio-button value="random">随机组题</a-radio-button>
                        </a-radio-group>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout" label="选择题库">
                        <a-select
                            v-decorator="[
                                'banks',
                                {
                                    rules: [{ required: true, message: '请至少选择一个题库' }]
                                }
                            ]"
                            mode="multiple"
                            placeholder="选择一个或多个题库吧"
                        >
                            <a-select-opt-group>
                                <span slot="label"><a-icon type="smile"/>中医类</span>
                                <a-select-option value="中医基础理论">中医基础理论</a-select-option>
                                <a-select-option value="医古文">医古文</a-select-option>
                            </a-select-opt-group>
                            <a-select-opt-group>
                                <span slot="label"><a-icon type="appstore"/>西医类</span>
                                <a-select-option value="免疫学">免疫学</a-select-option>
                                <a-select-option value="组织学与胚胎学">组织学与胚胎学</a-select-option>
                                <a-select-option value="生物化学">生物化学</a-select-option>
                            </a-select-opt-group>
                        </a-select>
                    </a-form-item>
                    <a-form-item v-if="form_bank.getFieldValue('type') == 'total' || !form_bank.getFieldValue('type')" v-bind="formItemLayout" label="题型选择" style="margin-bottom: 0">
                        <a-checkbox
                            v-decorator="[
                                'questionType',
                                {
                                    valuePropName: 'checked',
                                    initialValue: true,
                                    getValueFromEvent: checkAllQuestionType
                                }
                            ]"
                            :indeterminate="indeterminate"
                        >
                            全部
                        </a-checkbox>
                        <a-form-item>
                            <a-checkbox-group
                                v-decorator="[
                                    'questionTypeOption',
                                    {
                                        initialValue: questionType,
                                        getValueFromEvent: checkQuestionType
                                    }
                                ]"
                                :options="questionType"
                            />
                        </a-form-item>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout" v-if="form_bank.getFieldValue('type') == 'random'">
                        <span slot="label">
                            题型占比&nbsp;
                            <a-tooltip title="注意：【问答题】不会进行答案核对，【填空题】只有精准核对，没有模糊核对">
                                <a-icon type="question-circle-o" />
                            </a-tooltip>
                        </span>
                        <a-form-item label="单选-A型题目" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'singleA',
                                    {
                                        initialValue: 17
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
                                        initialValue: 17
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
                                        initialValue: 17
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
                                        initialValue: 17
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
                                        initialValue: 16
                                    }
                                ]"
                                :tipFormatter="rangeFormatter"
                                :marks="marks" 
                            />
                        </a-form-item>
                        <a-form-item label="问答" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'qa',
                                    {
                                        initialValue: 16
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
import { mapState, mapActions } from 'vuex'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
        form_bank: this.$form.createForm(this),
        marks: {
            0: '0',
            16: '16%',
            50: '50%',
            100: '100%',
        },
        indeterminate: false,
        formItemLayout: {
            labelCol: {
                span: 9
            },
            wrapperCol: {
                span: 8
            },
        },
        tailFormItemLayout: {
            wrapperCol: {
                md: {
                    span: 10,
                    offset: 7,
                },
                sm: {
                    span: 10,
                    offset: 6
                }
            }
        }
    }
  },
  async asyncData({ $axios }) {
    let userBaseInfo = null

    await $axios.get('getUserBaseInfo')
    .then((response) => {
        userBaseInfo = response.data
    })

    return {
        userBaseInfo: userBaseInfo,
    }
  },
  methods: {
      ...mapActions({
          setBank: 'bank/setBank'
      }),
      checkAllQuestionType(e) {
          this.indeterminate = false
          this.form_bank.setFieldsValue({
              'questionTypeOption': e.target.checked ? this.questionType : []
          })
          return e.target.checked
      },
      checkQuestionType(checkedList) {
          this.indeterminate = !!checkedList.length && (checkedList.length < this.questionType.length)
          this.form_bank.setFieldsValue({
              'questionType': checkedList.length === this.questionType.length
          })
          return checkedList
      },
      submitBank(e) {
          e.preventDefault()
          this.form_bank.validateFields((err, values) => {
              if (!err) {
                  let { singleA,singleB,multiple,blank,judge,qa } = this.form_bank.getFieldsValue(['singleA', 'singleB', 'multiple', 'blank', 'judge', 'qa'])
                  if (this.userBaseInfo.uid == -1) {
                      this.$message.warning('先登录吧～')
                  }
                  else if (singleA+singleB+multiple+blank+judge+qa > 100) {
                      this.$message.warning('题型占比超过100%, 请检查')
                  }
                  else if (singleA+singleB+multiple+blank+judge+qa < 100) {
                      this.$message.warning('题型占比不足100%, 请检查')
                  }
                  else {
                      this.$axios.post('submitBank', qs.stringify({
                          type: values.type,
                          banks: values.banks,
                          singleA: values.singleA,
                          singleB: values.singleB,
                          multiple: values.multiple,
                          blank: values.blank,
                          judge: values.judge,
                          qa: values.qa,
                          questionType: values.questionTypeOption
                      }, { arrayFormat: 'brackets' }))
                      .then((response) => {
                          if (response.data == 1) {
                              this.$message.error('未知错误')
                          }
                          else {
                              console.log(response.data.info)
                              this.setBank({ 'questions': response.data.info, 'timer': values.timer })
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
  computed: mapState({
      questionType: state => state.bank.questionType
  })
}
</script>

<style scoped>
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
</style>
