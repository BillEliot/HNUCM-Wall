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
                                            validator: validator_password2,
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
                                    'password2',
                                    {
                                        rules: [{
                                            required: true, message: '请输入密码',
                                        }, {
                                            validator: validator_password,
                                        }],
                                    }
                                ]"
                                type="password"
                                @blur="blur_password2"
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
                                    'class',
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
                                        rules: [{
                                            validator: validator_phone
                                        }]
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
                                    'qq'
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
                                    <a-button @click="getCaptcha">获取</a-button>
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
                            <a-button type="primary" html-type="submit" :disabled="!form_register.getFieldValue('agreement')" style="width: 100%">注册</a-button>
                        </a-form-item>
                    </a-form>
                </div>
            </div>
        </div>
	</div>
</template>

<script>
import qs from 'qs'
import md5 from 'js-md5'
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
    blur_password2 (e) {
        var value = e.target.value
        this.confirmDirty = this.confirmDirty || !!value
    },
    validator_password (rule, value, callback) {
        if (value && value !== this.form_register.getFieldValue('password')) {
            callback('两次密码不一致')
        } else {
            callback()
        }
    },
    validator_password2 (rule, value, callback) {
      if (value && this.confirmDirty) {
          this.form_register.validateFields(['password2'], { force: true })
      }
      callback()
    },
    validator_phone (rule, value, callback) {
        var regex_phone = /^1[34578]\d{9}$/
        if (value && !regex_phone.test(value)) {
            callback('请输入合法的手机号')
        }
        callback()
    },
    register(e) {
        e.preventDefault()
        this.form_register.validateFields((err, values) => {
            if (!err) {
                this.$axios.post('/register', qs.stringify({
                    email: values.email,
                    password: md5(values.password),
                    nickname: values.nickname,
                    bio: values.bio,
                    class: values.class,
                    phone: values.phone,
                    qq: values.qq,
                    wechat: values.wechat,
                    captcha: values.captcha
                }))
                .then((response) => {
                    if (response.data == 1) {
                        this.$message.error('验证码错误')
                    }
                    else if (response.data == 2) {
                        this.$message.error('电子邮件已存在')
                    }
                    else if (response.data == 3) {
                        this.$message.error('非法昵称')
                    }
                    else if (response.data == 4) {
                        this.$message.error('昵称已存在')
                    }
                    else if (response.data == 5) {
                        this.$message.error('未知错误')
                    }
                    else if (response.data == 0) {
                        this.$message.success('注册成功')
                        this.$router.push({ path: '/login' })
                    }
                })
            }
        })
    },
    getCaptcha() {
        var email = this.form_register.getFieldValue('email')
        if (email) {
            this.$axios.post('getCaptcha', qs.stringify({
                email: email
            }))
            .then((response) => {
                if (response.data == 0) {
                    this.$message.success('验证码已发往您的邮箱，请查收')
                }
                else {
                    this.$message.error('发送失败, 请稍后重试或联系站长')
                }
            })
        }
        else {
            this.$message.error('请输入您的邮箱')
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
