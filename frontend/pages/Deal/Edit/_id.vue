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
                            <h1>编辑物品</h1>
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
                        <a-form-item v-bind="formItemLayout" label="物品名称">
                            <a-input
                                v-decorator="[
                                    'name', {
                                        rules: [{ required: true, message: '请输入要交易的物品名称' }],
                                        initialValue: this.dealDetail.name
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
                                        rules: [
                                            { required: true, message: '请输入最低接受价格' },
                                            { type: 'number', message: '价格必须为数字' },
                                            { validator: validatorPrice}
                                        ],
                                        initialValue: this.dealDetail.price
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
                                        rules: [{ required: true, message: '选择一个新度哦～' }],
                                        initialValue: this.dealDetail.new
                                    }
                                ]"
                                allowHalf
                                :allowClear="false"
                            />
                            <span v-if="form_deal.getFieldValue('new')">{{ form_deal.getFieldValue('new')*2 }} 成新</span>
                            <span v-else>{{ this.dealDetail.new }} 成新</span>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品描述">
                            <a-textarea 
                                placeholder="对物品的描述"
                                :rows="4"
                                v-decorator="[
                                    'description', {
                                        rules: [{ required: true, message: '描述越详细，越容易卖出哦～' }],
                                        initialValue: this.dealDetail.description
                                    }
                                ]"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品照片">
                            <a-upload
                                v-decorator="[
                                    'uploader', {
                                        valuePropName: 'fileList',
                                        getValueFromEvent: uploadImages
                                    }
                                ]"
                                name="files"
                                accept='.jpg, .jpeg, .png'
                                listType="picture-card"
                                :multiple='true'
                                :supportServerRender='true'
                                :action="baseUrl + '/api/uploadDealImg'"
                                @preview="previewImage"
                            >
                                <div v-if="!form_deal.getFieldValue('uploader') || (form_deal.getFieldValue('uploader') && form_deal.getFieldValue('uploader').length < 3)">
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
      form_deal: this.$form.createForm(this),
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
  async asyncData({ $axios, redirect, query }) {
      let userBaseInfo = null

      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
          if (userBaseInfo.uid == -1) {
              redirect({ path: '/deal' })
          }
      })
      
      let dealDetail = null
      await $axios.post('getDealDetail', qs.stringify({
          id: query.id
      }))
      .then((response) => {
          if (response.data == 1) {
              redirect('/deal')
          }
          else {
              dealDetail = response.data
          }
      })

      return {
          userBaseInfo: userBaseInfo,
          dealDetail: dealDetail
      }
  },
  mounted() {
      let fileList = []
      this.dealDetail.images.forEach((url, index) => {
          fileList.push({
              uid: (0-index).toString(),
              name: (0-index).toString() + '.jpg',
              status: 'done',
              url: this.baseUrl + url
          })
      })
      this.form_deal.setFieldsValue({ 'uploader': fileList })
  },
  methods: {
      validatorPrice (rule, value, callback) {
          if (value < 0) {
              callback('最低价格为 ¥0')
          }
          callback()
      },
      uploadImages(e) {
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
              this.$axios.post('removeDealImg', qs.stringify({
                  url: e.file.url
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
          return e && e.fileList
      },
      previewImage(file) {
          this.previewImageUrl = file.url || file.thumbUrl
          this.previewImgVisible = true
      },
      editDeal(e) {
          e.preventDefault()
          this.form_deal.validateFields((err, values) => {
              if (!err) {
                  var images = []
                  values.uploader.forEach(file => {
                      images.push(file.name)
                  })

                  this.$axios.post('editDeal', qs.stringify({
                      id: this.dealDetail.id,
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
                      else if (response.data == 2) {
                          this.$message.warning('无权修改')
                      }
                      else {
                          this.$message.success('成功修改交易～')
                          this.$router.push({ path: '/deal/detail', query: { id: this.dealDetail.id } })
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

<style scoped>
a {
    text-decoration: none
}
</style>
