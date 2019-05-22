<template>
    <div class="container">
		<div class="row">
            <div class="col-md-6 col-md-offset-3">
                <div class="fh5co-form">
                    <a-form :form="form_register" @submit="register">
                        <a-form-item v-bind="formItemLayout" label="E-mail">
                            <a-input
                                v-decorator="[
                                    'email',
                                    {
                                        rules: [{
                                            type: 'email', message: '请输入有效的EMail',
                                        }, 
                                        {
                                            required: true, message: '请输入EMail',
                                        }]
                                    }
                                ]"
                            >
                                <a-icon slot="prefix" type="mail" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="密码">
                            <a-input
                                v-decorator="[
                                    'password',
                                    {
                                        rules: [{
                                            required: true, message: '请输入密码',
                                        },
                                        {
                                            validator: validateToNextPassword,
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
                                    'confirm',
                                    {
                                        rules: [{
                                            required: true, message: '请输入密码',
                                        }, {
                                            validator: compareToFirstPassword,
                                        }],
                                    }
                                ]"
                                type="password"
                                @blur="handleConfirmBlur"
                            >
                                <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout">
                            <span slot="label">
                                昵称&nbsp;
                                <a-tooltip title="其他人将会看到您的昵称">
                                    <a-icon type="question-circle-o" />
                                </a-tooltip>
                            </span>
                            <a-input
                                v-decorator="[
                                    'nickname',
                                    {
                                        rules: [{ required: true, message: '请输入昵称', whitespace: true }]
                                    }
                                ]"
                            >
                                <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout">
                            <span slot="label">
                                个性签名&nbsp;
                                <a-tooltip title="简略的最自己的描述">
                                    <a-icon type="question-circle-o" />
                                </a-tooltip>
                            </span>
                            <a-input
                                v-decorator="[
                                    'bio',
                                    {
                                        rules: [{ required: true, message: '请输入个性签名', whitespace: true }]
                                    }
                                ]"
                            >
                                <a-icon slot="prefix" type="edit" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="班级">
                            <a-cascader
                                v-decorator="[
                                    'residence',
                                    {
                                        initialValue: ['zhongyi', 'wuyi'],
                                        rules: [{ type: 'array', required: true, message: '请选择您的班级' }],
                                    }
                                ]"
                                :options="classes"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="手机" extra="可以和TA更密切的交流">
                            <a-input
                                v-decorator="[
                                'phone',
                                {
                                }
                                ]"
                                type="number"
                            >
                                <a-icon slot="prefix" type="phone" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="QQ" extra="可以和TA更密切的交流">
                            <a-input
                                v-decorator="[
                                'qq',
                                {
                                }
                                ]"
                                type="number"
                            >
                                <a-icon slot="prefix" type="qq" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="微信" extra="可以和TA更密切的交流">
                            <a-input
                                v-decorator="[
                                'wechat',
                                {
                                }
                                ]"
                            >
                                <a-icon slot="prefix" type="wechat" style="color:rgba(0,0,0,.25)" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="验证码" extra="验证码会发往您的邮箱">
                            <a-row :gutter="8">
                                <a-col :span="12">
                                    <a-input
                                        v-decorator="[
                                        'captcha',
                                        { rules: [{ required: true, message: '请输入验证码' }] }
                                        ]"
                                    />
                                    </a-col>
                                    <a-col :span="12">
                                    <a-button>获取</a-button>
                                </a-col>
                            </a-row>
                        </a-form-item>
                        <a-form-item v-bind="tailFormItemLayout">
                            <a-checkbox
                                v-decorator="[
                                    'agreement',
                                    { valuePropName: 'checked' }
                                ]"
                            >
                                我同意
                            </a-checkbox>
                            <a @click="showDrawer_agreement=true">用户条款</a>
                            <a-drawer
                                title="用户条款"
                                placement="right"
                                :closable="false"
                                @close="showDrawer_agreement=false"
                                :visible="showDrawer_agreement"
                            >
                                <p>Some contents...</p>
                            </a-drawer>
                        </a-form-item>
                        <a-form-item v-bind="tailFormItemLayout">
                            <a>已有账号？现在登录～</a>
                            <a-button type="primary" html-type="submit" style="width: 100%">注册</a-button>
                        </a-form-item>
                    </a-form>
                </div>
            </div>
        </div>
	</div>
</template>

<script>
import qs from 'qs'
//import md5 from 'js-md5'
//import Cookies from 'js-cookie'
import { mapState } from 'vuex'


export default {
  name: 'Register',
  data () {
    return {
        form_register: this.$form.createForm(this),
        confirmDirty: false,
        showDrawer_agreement: false,
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
                    span: 12,
                    offset: 6,
                },
            },
        },
    }
  },
  methods: {
    handleConfirmBlur (e) {
        const value = e.target.value
        this.confirmDirty = this.confirmDirty || !!value
    },
    compareToFirstPassword (rule, value, callback) {
        const form = this.form_register;
        if (value && value !== form.getFieldValue('password')) {
            callback('两次密码不一致')
        } else {
            callback()
        }
    },
    validateToNextPassword (rule, value, callback) {
      const form = this.form_register;
      if (value && this.confirmDirty) {
          form.validateFields(['confirm'], { force: true })
      }
      callback()
    },
    register() {
        var cities = this.cities
        var city = this.city.map(function (value, index, array) {
            for (var itm of cities) {
                if (itm.value == value) { cities = itm.children; return itm; }
            }
            return null;
        })

        this.$axios.post('/register', qs.stringify({
            'username': this.username,
            'truename': this.truename,
            'password': md5(this.password),
            'email': this.email,
            'school': this.school,
            'city': city[0].label + '/' + city[1].label + '/' + city[2].label,
            'identity': this.identity,
            'qq': this.qq,
            'wechat': this.wechat,
            'phone': this.phone,
            'smsCode': this.smsCode,
            'encrySmsCode': Cookies.get('encrySmsCode')
        }))
        .then((response) => {
            this.loding = false
            if (response.data == 1) {
                this.$message({
                    message: '用户名已存在',
                    type: 'error'
                })
            }
            else if (response.data == 2) {
                this.$message({
                    message: '电子邮件已存在',
                    type: 'error'
                })
            }
            else if (response.data == 3) {
                this.$message({
                    message: '手机已存在',
                    type: 'error'
                })
            }
            else if (response.data == 4) {
                this.$message({
                    message: '验证码错误',
                    type: 'error'
                })
            }
            else if (response.data == 0) {
                this.$message({
                    message: '注册成功',
                    type: 'success'
                })
                this.$router.push({path: '/login'})
            }
        })
    },
    getSmsCode() {
      if (this.phone) {
        var time = 60
        this.smsCodeDisabled = true
        var countDown = window.setInterval(() => {
            time--
            this.smsCodeText = time + 's后重新发送'
            if (time <= 0) {
                window.clearInterval(countDown)
                this.smsCodeDisabled = false
                this.smsCodeText = "获取验证码"
            }
            }, 1000)
        
        this.$axios.post('/getSmsCode', qs.stringify({
          'phone': this.phone
        }))
        .then((response) => {
            if (response.data.response != 'OK') {
                this.$message.error('短信发送失败')
            }
            else {
                this.$message.success('短信已发送')
                Cookies.set('encrySmsCode', response.data.code)
            }
        })
      }
      else {
        this.$message({
          message: '请输入手机号',
          type: 'error'
        })
      }
    }
  },
  computed: mapState({
    classes: state => state.classes,
  })
}
</script>

<style>
</style>
