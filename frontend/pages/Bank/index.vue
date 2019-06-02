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
                            刷题方式&nbsp;
                            <a-tooltip title="初期你可以刷全部题库，后期可以选择随机组题来检验自己">
                                <a-icon type="question-circle-o" />
                            </a-tooltip>
                        </span>
                        <a-select
                            v-decorator="[
                                'type',
                                {
                                    initialValue: 'total'
                                }
                            ]"
                        >
                            <a-select-option value="total">全部题库</a-select-option>
                            <a-select-option value="random">随机组题</a-select-option>
                        </a-select>
                    </a-form-item>
                    <a-form-item v-if="form_bank.getFieldValue('type') == 'total' || !form_bank.getFieldValue('type')" v-bind="formItemLayout" label="组题策略">
                        <a-radio-group
                            v-decorator="[
                                'method',
                                {
                                    initialValue: 'order'
                                }
                            ]"
                            buttonStyle="solid"
                        >
                            <a-radio-button value="order">顺序组题</a-radio-button>
                            <a-radio-button value="range">范围组题</a-radio-button>
                        </a-radio-group>
                    </a-form-item>
                    <a-form-item v-bind="formItemLayout" v-if="form_bank.getFieldValue('method') == 'range'">
                        <span slot="label">
                            题库范围&nbsp;
                            <a-tooltip title="如果您选择了多个题库，那么范围选择会作用于各个题库">
                                <a-icon type="question-circle-o" />
                            </a-tooltip>
                        </span>
                        <a-slider
                            v-decorator="[
                                'range',
                                {
                                    initialValue: [0, 100],
                                    rules: [{ validator: validatorRange }]
                                }
                            ]"
                            range
                            :tipFormatter="rangeFormatter"
                        />
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
                                <a-select-option value="组织学与胚胎学">组织学与胚胎学</a-select-option>
                                <a-select-option value="生物化学">生物化学</a-select-option>
                            </a-select-opt-group>
                        </a-select>
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
import { mapActions } from 'vuex'
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
        formItemLayout: {
            labelCol: {
                span: 8
            },
            wrapperCol: {
                span: 8
            },
        },
        tailFormItemLayout: {
            wrapperCol: {
                md: {
                    span: 10,
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
          setBank: 'setBank'
      }),
      validatorRange(rule, value, callback) {
          if (value[0] == value[1]) {
              callback('范围不对哦～')
          }
          callback()
      },
      submitBank(e) {
          e.preventDefault()
          this.form_bank.validateFields((err, values) => {
              if (!err) {
                  if (this.userBaseInfo.uid == -1) {
                      this.$message.warning('先登录吧～')
                  }
                  else {
                      this.$axios.post('submitBank', qs.stringify({
                          type: values.type,
                          method: values.method,
                          range: values.range,
                          banks: values.banks
                      }))
                      .then((response) => {
                          if (response.data == 1) {
                              this.$message.error('未知错误')
                          }
                          else {
                              this.setBank(response.data.questions, values.timer)
                          }
                      })
                  }
              }
          })
      },
      rangeFormatter(value) {
          return `${value} %`
      }
  }
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
</style>
