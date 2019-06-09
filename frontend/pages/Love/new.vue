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
                    <a-button type="primary" @click="$router.push({ path: '/love' })"><a-icon type="left" />返回</a-button>
                    <a-form :form="form_love" @submit="submitLove">
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
                            <a-select
                                v-decorator="[
                                    'userTo',
                                    { rules: [{ required: true, message: '请输入要表白的人的email或昵称' }] }
                                ]"
                                :showSearch="true"
                                placeholder="要表白的人的昵称"
                                style="width: 100%"
                                :filterOption="false"
                                @search="searchUser"
                                :notFoundContent="searchingUser ? undefined : null"
                            >
                                <a-spin v-if="searchingUser" slot="notFoundContent" size="small"/>
                                <a-select-option v-for="user in users" :key="user">{{ user }}</a-select-option>
                            </a-select>
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
                            <a-upload
                                v-decorator="[
                                    'uploader', 
                                    {
                                        valuePropName: 'fileList',
                                        getValueFromEvent: uploadImages,
                                    }]"
                                name="files"
                                accept='.jpg, .jpeg, .png'
                                listType="picture-card"
                                :multiple='true'
                                :supportServerRender='true'
                                :action="baseUrl + '/api/uploadLoveImg'"
                                @preview="previewImg"
                            >
                                <div v-if="!form_love.getFieldValue('uploader') || (form_love.getFieldValue('uploader') && form_love.getFieldValue('uploader').length < 3)">
                                    <a-icon type="plus" />
                                    <div>上传</div>
                                </div>
                            </a-upload>
                            <a-modal :visible="previewImgVisible" :footer="null" @cancel="previewImgVisible = false">
                                <img style="width: 100%" :src="previewImageUrl" />
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
import { mapState } from 'vuex'
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
      searchingUser: false,
      previewImgVisible: false,
      previewImageUrl: null,
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 10 },
        },
        wrapperCol: {
          xs: { span: 24 },
          sm: { span: 8 },
        },
      },
      tailFormItemLayout: {
        wrapperCol: {
          xs: {
            span: 24,
            offset: 0,
          },
          sm: {
            span: 10,
            offset: 10,
          }
        }
      },
    }
  },
  async asyncData({ $axios, error }) {
      let userBaseInfo = null
      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
          if (userBaseInfo.uid == -1) {
              error({ statusCode: 403, message: '先登录吧～' })
          }
      })
      
      return {
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      searchUser(value) {
          this.searchingUser = true
          this.$axios.post('searchUser', qs.stringify({
              user: value
          }))
          .then((response) => {
              this.searchingUser = false
              this.users = response.data.info
          })
      },
      uploadImages(e) {
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
      previewImg(file) {
          this.previewImageUrl = file.url || file.thumbUrl
          this.previewImgVisible = true
      },
      submitLove(e) {
          e.preventDefault()
          this.form_love.validateFields((err, values) => {
              if (!err) {
                  var images = []
                  values.uploader.forEach((file) => {
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
                          this.$router.push({ path: '/love' })
                      }
                  })
              }
          })
      },
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style>
</style>
