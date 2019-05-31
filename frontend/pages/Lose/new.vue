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
                            <p class="warning">若您还未完善联系资料(qq, 微信或电话), 请尽快完善, 这样拾取者可迅速联系到您</p>
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="丢失时间">
                            <a-date-picker 
                                v-decorator="[
                                    'date',
                                    {
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
                                    'name',
                                    {
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
                                    'description',
                                    { rules: [{ required: true, message: '描述越详细，越容易找到哦～' }] }
                                ]"
                            />
                        </a-form-item>
                        <a-form-item v-bind="formItemLayout" label="物品照片">
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
                                :action="baseUrl + '/api/uploadLoseImg'"
                                @preview="previewImage"
                            >
                                <div v-if="!form_lose.getFieldValue('uploader') || (form_lose.getFieldValue('uploader') && form_lose.getFieldValue('uploader').length < 3)">
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
import moment from 'moment'
import Footer from '~/components/footer.vue'
import navbar from '~/components/navbar'

export default {
  components: {
      Footer,
      navbar
  },
  data() {
    return {
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
  async asyncData({ $axios, redirect }) {
      let userBaseInfo = null

      await $axios.get('getUserBaseInfo')
      .then((response) => {
          userBaseInfo = response.data
          if (userBaseInfo.uid == -1) {
              redirect({ path: '/lose' })
          }
      })
      
      return {
          userBaseInfo: userBaseInfo
      }
  },
  methods: {
      moment,
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
              this.$axios.post('removeLoseImg', qs.stringify({
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
          return e && e.fileList
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
                      uid: this.userBaseInfo.uid,
                      date: values.date.format('YYYY-MM-DD HH:mm:ss'),
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
