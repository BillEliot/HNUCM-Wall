<template>
    <div>
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
                                匿名&nbsp;
                                <a-tooltip title="其他人不会知道你的真实身份">
                                    <a-icon type="question-circle-o" />
                                </a-tooltip>
                            </span>
                            <a-switch
                                v-decorator="[
                                    'isAnony',
                                    {
                                        valuePropName: 'checked',
                                        initialValue: isEdit ? loveDetail.userFrom_id == -1 ? true : false : false,
                                    }
                                ]" />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="表白人">
                            <a-select
                                v-decorator="[
                                    'userTo', {
                                        initialValue: isEdit ? parseUserTo(loveDetail.userTo) : [],
                                        rules: [{ required: true, message: '请输入要表白的人的昵称' }]
                                    }
                                ]"
                                mode="tags"
                                :showArrow="false" 
                                placeholder="要表白的人的昵称"
                                @search="searchUser"
                                style="width: 100%"
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
                                    'content', {
                                        initialValue: isEdit ? loveDetail.content : '',
                                        rules: [{ required: true, message: '说点什么吧' }]
                                    }
                                ]"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="图片">
                            <a-upload
                                v-decorator="[
                                    'uploader', {
                                        valuePropName: 'fileList',
                                        initialValue: isEdit ? parseUploader(loveDetail.images) : [],
                                        getValueFromEvent: getUploadImageList
                                    }]"
                                name="image"
                                accept='.jpg, .jpeg, .png'
                                listType="picture-card"
                                :multiple="true"
                                :supportServerRender="true"
                                :withCredentials="true"
                                :action="baseUrl + '/api/uploadImage'"
                                :data="{
                                    directory: 'wall'
                                }"
                                :beforeUpload="beforeUploadImage"
                                @preview="previewImg"
                            >
                                <div v-if="!form_love.getFieldValue('uploader') || (form_love.getFieldValue('uploader') && form_love.getFieldValue('uploader').length < 9)">
                                    <a-icon type="plus" />
                                    <div>上传</div>
                                </div>
                            </a-upload>
                            <a-modal :visible="previewImgVisible" :footer="null" @cancel="previewImgVisible = false">
                                <img style="width: 100%" :src="previewImageUrl" />
                            </a-modal>
                        </a-form-item>
                        <a-form-item v-bind="tailFormItemLayout" extra="可以向管理员申请置顶。">
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
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  middleware: 'LoginRequired',
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
  async asyncData({ $axios, query }) {
      let loveDetail = null

      if (query.isEdit) {
          await $axios.get('getLoveDetail', {
              params: {
                  id: query.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  loveDetail = response.data.data
              }
          })
      }

      return {
          isEdit: query.isEdit,
          loveDetail: loveDetail
      }
  },
  methods: {
      searchUser(value) {
          this.searchingUser = true
          this.$axios.get('searchUser', {
              params: {
                  user: value
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.users = response.data.data
              }
              this.searchingUser = false
          })
      },
      beforeUploadImage(file, fileList) {
          let uploader = this.form_love.getFieldValue('uploader') ? this.form_love.getFieldValue('uploader') : []
          if (uploader.length + fileList.length > 9) {
              return new Promise((resolve, reject) => {
                  this.$message.warning('最多接受9张图片')
                  reject()
              })
          }
          else {
              return true
          }
      },
      getUploadImageList(e) {
          if (!e || !e.fileList) {
              return e
          }

          let status = e.file.status
          if (status === 'done') {
              this.$message.success(`${e.file.name} 上传成功`)
              e.fileList.forEach((file) => {
                  if (file.name == e.file.name) {
                      file.name = e.file.response.data.name
                      return e.fileList
                  }
              })
          } else if (status === 'error') {
              this.$message.error(`${e.file.name} 上传失败`)
          } else if (status === 'removed') {
              this.$axios.get('removeImage', {
                  params: {
                      name: e.file.name,
                      directory: 'wall'
                  }
              })
              .then((response) => {
                  if (response.data.code == 200 && response.data.status == 'success') {
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
                  if (!!values.uploader) {
                      var images = []
                      values.uploader.forEach((file) => {
                          images.push(file.name)
                      })
                  }
                  
                  this.$axios.post('submitLove', qs.stringify({
                      id: this.loveDetail.id,
                      isEdit: this.isEdit,
                      isAnony: values.isAnony,
                      userTo: values.userTo,
                      content: values.content,
                      images: images
                  }, { arrayFormat: 'brackets' }))
                  .then((response) => {
                      if (response.data == 1) {
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
      parseUserTo(userTo) {
          let users = []
          userTo.forEach((user) => {
              users.push(user.username)
          })
          return users
      },
      parseUploader(images) {
          let fileList = []
          images.forEach((image, index) => {
              fileList.push({
                  uid: -(index + 1),
                  name: image.split('/').pop(),
                  status: 'done',
                  url: this.baseUrl + '/media/' + image
              })
          })
          return fileList
      }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl,
      userBaseInfo: state => state.userBaseInfo
  })
}
</script>

<style>
</style>
