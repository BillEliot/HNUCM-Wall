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
                <div class="text-center notice">
                    <span>题库数据来源于练习册</span>
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
                                'banks',
                                {
                                    rules: [{ required: true, message: '请至少选择一个题库' }],
                                    getValueFromEvent: selectBank
                                }
                            ]"
                        >
                            <a-select-opt-group>
                                <span slot="label"><a-icon type="heat-map"/>中医类</span>
                                <a-select-option value="中医基础理论">中医基础理论</a-select-option>
                            </a-select-opt-group>
                            <a-select-opt-group>
                                <span slot="label"><a-icon type="stock"/>西医类</span>
                                <a-select-option value="免疫学">免疫学</a-select-option>
                            </a-select-opt-group>
                        </a-select>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout" label="选择子章">
                        <a-transfer
                            v-decorator="[
                                'transfer',
                                {
                                    rules: [{ validator: validatorTransfer }],
                                    getValueFromEvent: transferBanks
                                }
                            ]"
                            :dataSource="subBanks"
                            showSearch
                            :filterOption="subBankFilter"
                            :targetKeys="targetSubBanks"
                            :render="item => item.title"
                        >
                        </a-transfer>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout" label="题目总数">
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
                        <a-form-item label="问答" class="questionPercent">
                            <a-slider
                                v-decorator="[
                                    'qa',
                                    {
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
import { mapState, mapGetters, mapActions } from 'vuex'
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
        subBanks: [],
        targetSubBanks: [],
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
      validatorTransfer(rule, value, callback) {
          if (this.targetSubBanks.length == 0) {
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
              'qa': 100
          })
      },
      selectRandomBank() {
          this.form_bank.setFieldsValue({
              'singleA': 17,
              'singleB': 17,
              'multiple': 17,
              'blank': 17,
              'judge': 16,
              'qa': 16
          })
      },
      selectBank(value) {
          this.subBanks = this.getSubBanks(value)
          this.form_bank.setFieldsValue({
              'numQuestion': 0
          })
          this.maxNumQuestion = 0
          return value
      },
      transferBanks(targetKeys, direction, moveKeys) {
          this.targetSubBanks = moveKeys
          // get quantity of selected banks' question
          this.$axios.post('getNumQuestion', qs.stringify({
              banks: moveKeys
          }, { arrayFormat: 'brackets' }))
          .then((response) => {
              this.maxNumQuestion = response.data
              this.form_bank.setFieldsValue({
                  'numQuestion': response.data
              })
          })
      },
      subBankFilter(inputValue, option) {
          return option.title.indexOf(inputValue) > -1
      },
      submitBank(e) {
          e.preventDefault()
          this.form_bank.validateFields((err, values) => {
              if (!err) {
                  let { singleA,singleB,multiple,blank,judge,qa } = this.form_bank.getFieldsValue(['singleA', 'singleB', 'multiple', 'blank', 'judge', 'qa'])
                  if (this.userBaseInfo.uid == -1) {
                      this.$message.warning('先登录吧～')
                  }
                  else if (values.type == 'random' && singleA+singleB+multiple+blank+judge+qa > 100) {
                      this.$message.warning('题型占比超过100%, 请检查')
                  }
                  else if (values.type == 'random' && singleA+singleB+multiple+blank+judge+qa < 100) {
                      this.$message.warning('题型占比不足100%, 请检查')
                  }
                  else {
                      this.$axios.post('submitBank', qs.stringify({
                          type: values.type,
                          banks: this.targetSubBanks,
                          numQuestion: this.form_bank.getFieldValue('numQuestion'),
                          singleA: values.singleA,
                          singleB: values.singleB,
                          multiple: values.multiple,
                          blank: values.blank,
                          judge: values.judge,
                          qa: values.qa,
                      }, { arrayFormat: 'brackets' }))
                      .then((response) => {
                          if (response.data == 1) {
                              this.$message.error('未知错误')
                          }
                          else {
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
  computed: {
      ...mapState({
          banks: state => state.bank.banks
      }),
      ...mapGetters({
          getSubBanks: 'bank/getSubBanks'
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
</style>
