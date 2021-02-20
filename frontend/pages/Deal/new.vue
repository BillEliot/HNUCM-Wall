<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>发布物品</h1>
                            <p class="subheading">没有中间商赚差价～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- container -->
        <div class="container" style="margin-top: 50px">
            <div class="row">
                <div class="col-md-12">
                    <a-button type="primary" @click="$router.push({ path: '/deal' })"><a-icon type="left" />返回</a-button>
                    <a-form :form="form_deal" @submit="submitDeal">
                        <a-form-item v-bind="formItemLayout" label="注意">
                            <p class="warning">若您还未完善联系资料(qq, 微信或认证电话), 请尽快完善, 这样买家可迅速联系到您</p>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品名称">
                            <a-input
                                v-decorator="[
                                    'name', {
                                        initialValue: isEdit ? dealDetail.name : '',
                                        rules: [{ required: true, message: '请输入要交易的物品名称' }]
                                    }
                                ]"
                                placeholder="物品名称"
                            >
                                <a-icon slot="prefix" type="book" />
                            </a-input>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="最低接受价格">
                            <a-input-number
                                v-decorator="[
                                    'price', {
                                        initialValue: isEdit ? dealDetail.price : 0,
                                        rules: [
                                            { required: true, message: '请输入最低接受价格' },
                                            { type: 'number', message: '价格必须为数字' },
                                            { validator: validatorPrice}
                                        ]
                                    }
                                ]"
                                :formatter="value => `¥ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
                                :parser="value => value.replace(/\¥\s?|(,*)/g, '')"
                                style="width: 250px"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="新度">
                            <a-rate 
                                v-decorator="[
                                    'new', {
                                        initialValue: isEdit ? dealDetail.new : 4,
                                        rules: [{ required: true, message: '选择一个新度哦～' }]
                                    }
                                ]"
                                :tooltips="desc"
                                allowHalf
                                :allowClear="false"
                                @hoverChange="onRateHoverChange"
                                @change="onRateChange"
                            />
                            <span style="margin-left: 10px">{{ rate }} 成新</span>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品描述">
                            <a-textarea 
                                placeholder="对物品的描述"
                                :rows="4"
                                v-decorator="[
                                    'description', {
                                        initialValue: isEdit ? dealDetail.description : '',
                                        rules: [{ required: true, message: '描述越详细，越容易卖出哦～' }]
                                    }
                                ]"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品照片">
                            <a-upload
                                v-decorator="[
                                    'uploader', {
                                        valuePropName: 'fileList',
                                        initialValue: isEdit ? parseUploader(dealDetail.images) : [],
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
                                <div v-if="!form_deal.getFieldValue('uploader') || (form_deal.getFieldValue('uploader') && form_deal.getFieldValue('uploader').length < 9)">
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

export default {
  layout: 'common',
  middleware: 'LoginRequired',
  data() {
    return {
      form_deal: this.$form.createForm(this),
      desc: ['糟糕', '破损', '一般', '陈旧', '极好'],
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
      let dealDetail = null
      let rate = 8

      if (query.isEdit) {
          await $axios.get('getDealDetail', {
              params: {
                  id: query.id
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  dealDetail = response.data.data
                  rate = dealDetail.new * 2
              }
          })
      }

      return {
          isEdit: query.isEdit,
          dealDetail: dealDetail,
          rate: rate
      }
  },
  methods: {
      validatorPrice (rule, value, callback) {
          if (value < 0) {
              callback('最低价格为 ¥0')
          }
          callback()
      },
      beforeUploadImage(file, fileList) {
          let uploader = this.form_deal.getFieldValue('uploader') ? this.form_deal.getFieldValue('uploader') : []
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
      submitDeal(e) {
          e.preventDefault()
          this.form_deal.validateFields((err, values) => {
              if (!err) {
                  var images = []
                  values.uploader.forEach((file) => {
                      images.push(file.name)
                  })

                  this.$axios.post('submitDeal', qs.stringify({
                      id: this.dealDetail.id,
                      isEdit: this.isEdit,
                      name: values.name,
                      price: values.price,
                      new: values.new,
                      description: values.description,
                      images: images
                  }, { arrayFormat: 'brackets' }))
                  .then((response) => {
                      if (response.data == 1) {
                          this.$message.error('未知错误')
                      }
                      else {
                          this.$message.success('成功发布交易～')
                          this.$router.push({ path: '/deal' })
                      }
                  })
              }
          })
      },
      onRateHoverChange(number) {
          if (number) {
              this.rate = number * 2
          }
          else {
              this.rate = this.form_deal.getFieldValue('new') * 2
          }
      },
      onRateChange(number) {
          this.rate = number * 2
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
      baseUrl: state => state.baseUrl
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
