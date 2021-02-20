<template>
    <div>
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>找回密码</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <div class="container">
            <div class="row">
                <div class="col-md-6 col-md-offset-3">
                    <a-steps :current="step">
                        <a-step title="确认账号" />
                        <a-step title="重置密码" />
                        <a-step title="重置成功" />
                    </a-steps>
                    <hr />
                    <div v-show="step == 0">
                        <a-auto-complete placeholder="请输入绑定的邮箱" v-model="email" @search="handleSearch" style="width: 100%">
                            <template slot="dataSource">
                                <a-select-option v-for="email in result" :key="email">{{ email }}</a-select-option>
                            </template>
                        </a-auto-complete>
                        <a-button type="primary" @click="checkBoundEMail()" style="width: 100%; margin-top: 10px">确定</a-button>
                    </div>
                    <div v-show="step == 1">
                        <a-form :form="form_findpassword" @submit="findpassword">
                            <a-form-item v-bind="formItemLayout" label="密码">
                                <a-input
                                    v-decorator="[
                                        'password', {
                                            rules: [{
                                                required: true, message: '请输入密码',
                                            }, {
                                                validator: validator_password,
                                            }],
                                        }
                                    ]"
                                    type="password"
                                >
                                    <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="确认密码">
                                <a-input
                                    v-decorator="[
                                        'password2', {
                                            rules: [{
                                                required: true, message: '请输入密码',
                                            }, {
                                                validator: validator_password2,
                                            }],
                                        }
                                    ]"
                                    type="password"
                                    @blur="blur_password2"
                                >
                                    <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                                </a-input>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="邮箱">
                                <span>{{ email }}</span>
                            </a-form-item>
                            <a-form-item v-bind="formItemLayout" label="验证码">
                                <a-row :gutter="4">
                                    <a-col :span="16">
                                        <a-input
                                            v-decorator="['captcha', {
                                                rules: [{ required: true, message: '请输入验证码' }]
                                            }]"
                                        />
                                    </a-col>
                                    <a-col :span="8">
                                        <a-button :disabled="isDisableCaptcha" @click="getCaptcha">{{ CaptchaButtonText }}</a-button>
                                    </a-col>
                                </a-row>
                            </a-form-item>
                            <a-form-item v-bind="tailFormItemLayout">
                                <a-button type="primary" html-type="submit" style="width: 100%">确认修改</a-button>
                            </a-form-item>
                        </a-form>
                    </div>
                    <div v-show="step==2" class="text-center">
                        <span style="font-weight: bold; font-size: 32px; color: green">密码重置成功</span>
                        <br />
                        <a-button @click="this.$router.push({ path: '/' })">返回主页</a-button>
                        <a-button type="primary" @click="this.$router.push({ path: '/login' })">登录</a-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'

export default {
  layout: 'common',
  data() {
    return {
        step: 0,
        email: '',
        result: [],
        form_findpassword: this.$form.createForm(this),
        formItemLayout: {
            labelCol: {
                xs: { span: 24 },
                sm: { span: 6 },
            },
            wrapperCol: {
                xs: { span: 24 },
                sm: { span: 16 },
            },
        },
        tailFormItemLayout: {
            wrapperCol: {
                xs: {
                    span: 24,
                    offset: 0,
                },
                sm: {
                    span: 24,
                    offset: 0,
                },
            },
        },
        isDisableCaptcha: false,
        CaptchaButtonText: '获取'
    }
  },
  async asyncData({ store, redirect }) {
      if (store.state.userBaseInfo.id != -1) {
          redirect('/')
      }
  },
  methods: {
      handleSearch(value) {
          let result = []
          if (!!value && value.indexOf('@') == -1) {
              result = [
                  'qq.com',
                  '163.com',
                  '126.com',
                  'gmail.com',
                  'foxmail.com',
                  'sina.com',
                  'yeah.net',
                  'sohu.com',
                  'outlook.com',
                  'aliyun.com',
                  'yahoo.com'
              ].map(domain => `${value}@${domain}`)
          }
          this.result = result
      },
      checkBoundEMail() {
          if (!!this.email) {
              this.$axios.get('checkBoundEMail', {
                  params: {
                      email: this.email
                  }
              })
              .then((response) => {
                  if (response.data.code == 200 && response.data.status == 'success') {
                      this.step = 1
                  }
              })
          }
          else {
              this.$message.warning('请输入绑定的邮箱')
          }
      },
      blur_password2 (e) {
          let value = e.target.value
          this.confirmDirty = this.confirmDirty || !!value
      },
      validator_password (rule, value, callback) {
          if (value && this.confirmDirty) {
              this.form_findpassword.validateFields(['password2'], { force: true })
          }
          callback()
      },
      validator_password2 (rule, value, callback) {
          if (value && value !== this.form_findpassword.getFieldValue('password')) {
              callback('两次密码不一致')
          } else {
              callback()
          }
      },
      getCaptcha() {
        if (!!this.email) {
            this.$axios.get('getCaptcha', {
                params: {
                    email: this.email
                }
            })
            .then((response) => {
                if (response.data.code == 200 && response.data.status == 'success') {
                    this.$message.success('验证码已发往您的邮箱，有效期为3分钟，请查收')
                }
            })

            this.isDisableCaptcha = true
            let time = 60
            var countDown = setInterval(() => {
                time --
                if (time == 0) {
                    this.isDisableCaptcha = false
                    this.CaptchaButtonText = '获取'
                    clearInterval(countDown)
                }
                else {
                    this.CaptchaButtonText = time.toString() + '后重新获取'
                }
            }, 1000)
        }
        else {
            this.$message.error('请输入您的邮箱')
        }
      },
      findpassword(e) {
          e.preventDefault()
          this.form_findpassword.validateFields((err, values) => {
              if (!err) {
                this.$axios.post('findpassword', qs.stringify({
                    email: this.email,
                    password: values.password,
                    captcha: values.captcha
                }))
                .then((response) => {
                    if (response.data.code == 200 && response.data.status == 'success') {
                        this.step = 2
                    }
                })
              }
          })
      }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
