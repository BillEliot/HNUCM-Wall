<template>
  <div class="container">
    <div class="row">
      <div class="col-md-4 col-md-offset-4">
        <div class="fh5co-form">
          <a-tabs defaultActiveKey="1">
            <a-tab-pane tab="账号密码登录" key="1">
              <a-form :form="form_login" @submit="login">
                <a-form-item label="用户名" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                  <a-input v-decorator="[
                      'email',
                      { rules: [{ required: true, message: '请输入邮箱'}] }
                    ]"
                    placeholder="请输入邮箱">
                    <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
                  </a-input>
                </a-form-item>
                <a-form-item label="密码" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                  <a-input v-decorator="[
                      'password',
                      { rules: [{ required: true, message: '请输入密码'}] }
                    ]"
                    type="password" 
                    placeholder="请输入密码">
                    <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
                  </a-input>
                </a-form-item>
                <a-form-item>
                  <router-link to="/register">
                    <a style="float: right">忘记密码</a>
                  </router-link>
                  <router-link to="/register">
                    <a style="float: left">没有账号？注册一个吧～</a>
                  </router-link>
                  <a-button type="primary" html-type="submit" style="width: 100%">登录</a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>
            <a-tab-pane tab="短信验证码登录" key="2" forceRender>
                <a-form :form="form_SMS" @submit="sendSMS">
                    <a-form-item label="手机号" :label-col="{ span: 5 }" :wrapper-col="{ span: 18 }">
                        <a-input v-decorator="[
                              'phone',
                              { rules: [{ required: true, message: '请输入手机号'}] }
                            ]" 
                            type="number"
                            placeholder="请输入手机号">
                            <a-icon slot="prefix" type="phone" style="color:rgba(0,0,0,.25)" />
                        </a-input>
                    </a-form-item>
                    <a-form-item>
                        <a-button type="primary" html-type="submit" style="width: 100%">发送</a-button>
                    </a-form-item>
                </a-form>
            </a-tab-pane>
          </a-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import qs from "qs";
  import md5 from 'js-md5'

  export default {
    name: "Login",
    //middleware: 'auth',
    data() {
      return {
        form_login: this.$form.createForm(this),
        form_SMS: this.$form.createForm(this),
      }
    },
    methods: {
      login(e) {
        e.preventDefault()
        this.form_login.validateFields((err, values) => {
          if (!err) {
            this.$axios.post('/login', qs.stringify({
              email: values.email,
              password: md5(values.password)
            }))
            .then((response) => {
              if (response.data == 1) {
                this.$message.error('用户名不存在')
              }
              else if (response.data == 2) {
                this.$message.error('密码错误')
              } 
              else {
                this.$router.push({ path: '/' })
              }
            })
          }
        })
      },
      sendSMS() {

      }
    }
  }
</script>

<style>
</style>
