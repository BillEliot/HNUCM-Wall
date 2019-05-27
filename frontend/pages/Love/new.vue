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
                            <h1>告白吧</h1>
                            <p class="subheading">加油(ง •̀灬•́)ง</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- container -->
        <div class="container" style="margin-top: 50px">
            <div class="row">
                <div class="col-md-12">
                    <a-form
                        :form="form_love"
                        @submit="submitLove"
                    >
                        <a-form-item v-bind="formItemLayout">
                            <span slot="label">
                                启用匿名？&nbsp;
                                <a-tooltip title="其他人不会知道你的真实身份">
                                    <a-icon type="question-circle-o" />
                                </a-tooltip>
                            </span>
                            <a-switch
                                v-decorator="[
                                    'anony',
                                    {
                                        valuePropName: 'checked',
                                        initialValue: false,
                                    }
                                ]" />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="表白人">
                            <a-auto-complete
                                :dataSource="users"
                                style="width: 200px"
                                @search="searchUser"
                                placeholder="要表白的人的email或昵称"
                                v-decorator="[
                                    'userTo',
                                    { rules: [{ required: true, message: '请输入要表白的人的email或昵称' }] }
                                ]">
                            </a-auto-complete>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="表白语">
                            <a-textarea 
                                placeholder="表白吧～" 
                                :rows="4"
                                v-decorator="[
                                    'content',
                                    { rules: [{ required: true, message: '说点什么吧' }] }
                                ]"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="图片">
                            <a-upload-dragger
                                v-decorator="[
                                    'dragger', 
                                    {
                                        valuePropName: 'fileList',
                                        getValueFromEvent: uploadFile,
                                    }]"
                                    name="files"
                                    accept='.jpg, .jpeg, .png'
                                    listType='picture'
                                    :multiple='true'
                                    :supportServerRender='true'
                                    action="http://localhost:8000/api/uploadLoveImg"
                                    @preview='previewLoveImg'
                            >
                            <p class="ant-upload-drag-icon">
                                <a-icon type="inbox" />
                            </p>
                            <p class="ant-upload-text">
                                点击选择或拖拽图片
                            </p>
                            <p class="ant-upload-hint">
                                这些图片一定有着你对TA的思念吧～
                            </p>
                            </a-upload-dragger>
                            <a-modal :visible="previewLoveImgVisible" :footer="null" @cancel="previewLoveImgVisible = false">
                                <img style="width: 100%" :src="previewLoveImageUrl" />
                            </a-modal>
                        </a-form-item>
                        <a-form-item v-bind="tailFormItemLayout">
                            <a-button
                                type="primary"
                                html-type="submit"
                            >
                                表白 ஐ٩(๑´ᵕ`)۶ஐ
                            </a-button>
                        </a-form-item>
                    </a-form>
                </div>
            </div>
        </div>

        <Footer />

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
      form_love: this.$form.createForm(this),
      users: [],
      previewLoveImgVisible: false,
      previewLoveImageUrl: null,
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 8 },
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
            span: 16,
            offset: 8,
          }
        }
      },
    }
  },
  async asyncData({ $axios }) {
      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
      })
      
      return {
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      searchUser(value) {
          this.$axios.post('/searchUser', qs.stringify({
              user: value
          }))
          .then((response) => {
              this.users = response.data.info
          })
      },
      uploadFile(e) {
          if (!e || !e.fileList) {
            return e
          }

          let status = e.file.status
          if (status === 'done') {
              this.$message.success(`${e.file.name} 上传成功`)
              e.fileList.forEach((file) => {
                  if (file.name == e.file.name) {
                      file.name = e.file.response
                      return false
                  }
              })
          } else if (status === 'error') {
              this.$message.error(`${e.file.name} 上传失败`)
          } else if (status === 'removed') {
              this.$axios.post('removeLoveImg', qs.stringify({
                  name: e.file.name
              }))
              .then((response) => {
                  if (response.data == 0) {
                      this.$message.success(`${e.file.name} 删除成功`)
                  }
                  else {
                      this.$message.error(`${e.file.name} 删除失败`)
                  }
              })
          }
          return e.fileList
      },
      previewLoveImg(file) {
          this.previewLoveImageUrl = file.url || file.thumbUrl
          this.previewLoveImgVisible = true
      },
      submitLove(e) {
          e.preventDefault()
          this.form_love.validateFields((err, values) => {
              if (!err) {
                  var images = []
                  values.dragger.forEach((file) => {
                      images.push(file.name)
                  })

                  this.$axios.post('submitLove', qs.stringify({
                      anony: values.anony,
                      userTo: values.userTo,
                      content: values.content,
                      images: images
                  }, { arrayFormat: 'brackets' }))
                  .then((response) => {
                      if (response.data == 1) {
                          this.$message.error('非法数据')
                      }
                      else if (response.data == 2) {
                          this.$message.error('未知错误')
                      }
                      else {
                          this.$message.success('成功发布告白～')
                          this.$router.push({ path: '/' })
                      }
                  })
              }
          })
      },
  },
}
</script>

<style>
</style>
