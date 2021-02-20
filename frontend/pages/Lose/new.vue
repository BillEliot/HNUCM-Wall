<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>发布失物</h1>
                            <p class="subheading">现在很难过吧(ノへ￣、)</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- container -->
        <div class="container" style="margin-top: 50px">
            <div class="row">
                <div class="col-md-12">
                    <a-button type="primary" @click="$router.push({ path: '/lose' })"><a-icon type="left" />返回</a-button>
                    <a-form :form="form_lose" @submit="submitLose">
                        <a-form-item v-bind="formItemLayout" label="注意">
                            <p class="warning">若您还未完善联系资料(qq, 微信或认证电话), 请尽快完善, 这样拾取者可迅速联系到您</p>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="丢失时间">
                            <a-date-picker 
                                v-decorator="[
                                    'date', {
                                        initialValue: isEdit ? moment(loseDetail.loseDate) : '',
                                        rules: [{ required: true, message: '请选择丢失日期' }]
                                    }
                                ]"
                                format="YYYY-MM-DD HH:mm:ss"
                                :disabledDate="disabledDate"
                                :disabledTime="disabledTime"
                                :showTime="{ defaultValue: moment('00:00:00', 'HH:mm:ss') }"
                            >
                                <template slot="renderExtraFooter"></template>
                            </a-date-picker>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品名称">
                            <a-input
                                v-decorator="[
                                    'name', {
                                        initialValue: isEdit ? loseDetail.name : '',
                                        rules: [{ required: true, message: '请输入丢失的物品名称' }]
                                    }
                                ]"
                                placeholder="物品名称"
                            >
                                <a-icon slot="prefix" type="book" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品描述">
                            <a-textarea 
                                placeholder="对物品的描述" 
                                :rows="4"
                                v-decorator="[
                                    'description', {
                                        initialValue: isEdit ? loseDetail.description : '',
                                        rules: [{ required: true, message: '描述越详细，越容易找到哦～' }]
                                    }
                                ]"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品照片">
                            <a-upload
                                v-decorator="[
                                    'uploader', {
                                        valuePropName: 'fileList',
                                        initialValue: isEdit ? parseUploader(loseDetail.images) : [],
                                        getValueFromEvent: getUploadImageList,
                                    }]"
                                name="image"
                                accept='.jpg, .jpeg, .png'
                                listType="picture-card"
                                :multiple='true'
                                :supportServerRender='true'
                                :withCredentials="true"
                                :action="baseUrl + '/api/uploadImage'"
                                :data="{
                                    directory: 'wall'
                                }"
                                :beforeUpload="beforeUploadImage"
                                @preview="previewImage"
                            >
                                <div v-if="!form_lose.getFieldValue('uploader') || (form_lose.getFieldValue('uploader') && form_lose.getFieldValue('uploader').length < 9)">
                                    <a-icon type="plus" />
                                    <div>上传</div>
                                </div>
                            </a-upload>
                            <a-modal :visible="previewImgVisible" :footer="null" @cancel="previewImgVisible = false">
                                <img style="width: 100%" :src="previewImageUrl" />
                            </a-modal>
                        </a-form-item>
                        <a-form-item v-bind="tailFormItemLayout">
                            <a-button type="primary" html-type="submit">发布</a-button>
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
import moment from 'moment'

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  data() {
    return {
      moment,

      form_lose: this.$form.createForm(this),
      previewImgVisible: false,
      previewImageUrl: null,
      formItemLayout: {
        labelCol: {
          xs: { span: 24 },
          sm: { span: 5 },
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
            offset: 5,
          }
        }
      },
    }
  },
  async asyncData({ $axios, query }) {
      let loseDetail = null

      if (query.isEdit) {
          await $axios.get('getLoseDetail', {
              params: {
                  id: query.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  loseDetail = response.data.data
              }
          })
      }

      return {
          isEdit: query.isEdit,
          loseDetail: loseDetail
      }
  },
  methods: {
      dateRange(start, end) {
          var result = [];
          for (let i = start; i < end; i++) {
              result.push(i)
          }
          return result
      },
      disabledDate(current) {
          return current > moment().endOf('day')
      },
      disabledTime() {
          return {
              disabledHours: () => this.dateRange(moment().get('hours'), 24),
              disabledMinutes: () => this.dateRange(moment().get('minutes'), 60),
              disabledSeconds: () => this.dateRange(moment().get('seconds'), 60),
          }
      },
      beforeUploadImage(file, fileList) {
          let uploader = this.form_lose.getFieldValue('uploader') ? this.form_lose.getFieldValue('uploader') : []
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
      previewImage(file) {
          this.previewImageUrl = file.url || file.thumbUrl
          this.previewImgVisible = true
      },
      submitLose(e) {
          e.preventDefault()
          this.form_lose.validateFields((err, values) => {
              if (!err) {
                  var images = []
                  values.uploader.forEach((file) => {
                      images.push(file.name)
                  })

                  this.$axios.post('submitLose', qs.stringify({
                      id: this.loseDetail.id,
                      isEdit: this.isEdit,
                      loseDate: values.date.format('YYYY-MM-DD HH:mm:ss'),
                      name: values.name,
                      description: values.description,
                      images: images
                  }, { arrayFormat: 'brackets' }))
                  .then((response) => {
                      if (response.data == 1) {
                          this.$message.error('未知错误')
                      }
                      else {
                          this.$message.success('成功发布失物，祝您早日找回～')
                          this.$router.push({ path: '/lose' })
                      }
                  })
              }
          })
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

<style scoped>
a {
    text-decoration: none
}

.warning {
    font-weight: bold;
    color: red;
}
</style>
