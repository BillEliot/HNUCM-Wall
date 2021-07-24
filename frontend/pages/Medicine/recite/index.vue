<template>
    <div>
        <!-- drawer -->
        <a-drawer
            title="设置学习计划"
            placement="bottom"
            :height="512"
            :visible="showSettingDrawer"
            :body-style="{ paddingBottom: '80px' }"
            @close="showSettingDrawer = false"
        >
            <a-spin :spinning="spinning_plan">
                <a-form :form="form" layout="vertical" hide-required-mark>
                    <a-form-item label="章节">
                        <a-transfer
                            v-decorator="[
                                'chapter',
                                {
                                    rules: [{ validator: validatorTransfer }]
                                }
                            ]"
                            :data-source="allChapters"
                            show-search
                            :operations="['添加', '删除']"
                            :target-keys="targetChapters"
                            :render="item => `${item.key}`"
                            @change="changeChapter"
                        >
                        </a-transfer>
                        <span>
                            共
                            <span style="font-weight: bold; color: green">{{ maxChapters }}</span>
                            味中药
                        </span>
                    </a-form-item>
                    <a-form-item label="每日背诵量">
                        <a-slider
                            v-decorator="[
                                'amount',
                                {
                                    initialValue: 0,
                                }
                            ]"
                            :min="1"
                            :max="maxChapters"
                        />
                        <span>
                            每日背诵
                            <span style="font-weight: bold; color: green">{{ this.form.getFieldValue('amount') }}</span>
                            味，
                            复习
                            <span style="font-weight: bold; color: green">{{ Math.floor(this.form.getFieldValue('amount') / 2) }}</span>
                            味，
                            需要
                            <span style="font-weight: bold; color: green">{{ Math.ceil(maxChapters / this.form.getFieldValue('amount')) }}</span>
                            天完成
                        </span>
                    </a-form-item>
                    <a-form-item label="是否乱序">
                        <a-checkbox
                            v-decorator="[
                                'isRandom',
                                {
                                    valuePropName: 'checked',
                                    initialValue: true
                                }
                            ]">
                        </a-checkbox>
                    </a-form-item>
                </a-form>
            </a-spin>
            <a-divider />
            <div style="width: '100%'; zIndex: 1">
                <a-button :style="{ marginRight: '8px' }" @click="showSettingDrawer = false">取消</a-button>
                <a-button type="primary" @click="submit">确定</a-button>
            </div>
        </a-drawer>

        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>背中药</h1>
                            <p class="subheading">持之以恒</p>
                            <a-divider />
                            <a-button v-show="tabKey != 0 && tabKey != 1" type="primary" @click="tabKey = 1">返回</a-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <a-row v-if="tabKey == 0" type="flex" justify="center">
                <a-col>
                    <p style="color: green; font-weight: bold">您还未设置学习计划!</p>
                    <a-button type="primary" size="large" @click="showSettingDrawer = true">设置学习计划</a-button>
                </a-col>
            </a-row>
            <div v-else-if="tabKey == 1">
                <a-row type="flex" justify="center">
                    <a-col :md="10" :sm="12" :xs="24">
                        <div>
                            <span style="font-weight: bold; color: green; font-size: 48px">{{ reciteSetting.signDays }}</span>天
                            <a-button type="link" @click="$router.push({ path: '/medicine/recite/log' })">打卡记录</a-button>
                            <a-button type="link" @click="changePlan()">修改学习计划</a-button>
                        </div>
                        <a-collapse>
                            <a-collapse-panel key="1" header="所选章节">
                                <p>{{ reciteSetting.chapters }}</p>
                            </a-collapse-panel>
                        </a-collapse>
                        <div style="margin-top: 10px">
                            <a-progress
                                :stroke-color="{
                                    from: '#108ee9',
                                    to: '#87d068',
                                }"
                                :percent="(reciteSetting.recitedAmount / reciteSetting.totalAmount * 100).toFixed(2)"
                                status="active"
                            />
                            <div style="float: right">
                                {{ reciteSetting.recitedAmount }} / {{ reciteSetting.totalAmount }}
                            </div>
                            <div style="float: left">
                                预计还有{{ Math.ceil(((reciteSetting.totalAmount - reciteSetting.recitedAmount) / reciteSetting.everydayAmount)) }}天学完
                            </div>
                        </div>
                    </a-col>
                </a-row>
                <a-divider>今日任务</a-divider>
                <a-row type="flex" justify="center" class="text-center">
                    <a-col :md="4" :sm="10" :xs="8">
                        <a-card title="需新学">
                            <span>{{ reciteSetting.todayWillReciteAmount }}</span>
                        </a-card>
                    </a-col>
                    <a-col :md="4" :sm="10" :xs="8">
                        <a-card title="需复习">
                            <span>{{ reciteSetting.todayWillReviewAmount }}</span>
                        </a-card>
                    </a-col>
                    <a-col :md="4" :sm="10" :xs="8">
                        <a-card title="未学">
                            <span>{{ reciteSetting.todayUnlearnedAmount }}</span>
                        </a-card>
                    </a-col>
                </a-row>
                <a-row type="flex" justify="center">
                    <a-col :md="8" :sm="12" :xs="24">
                        <a-divider></a-divider>
                        <a-button type="primary" @click="start" style="width: 100%">开始学习</a-button>
                    </a-col>
                </a-row>
            </div>
            <div v-else-if="tabKey == 2" class="text-center">
                <a-row type="flex" justify="center">
                    <a-col :md="4" :sm="12" :xs="12">
                        <a-statistic title="今日复习" :value="todayReviewAmount + '/' + todayWillReviewAmount"></a-statistic>
                    </a-col>
                    <a-col :md="4" :sm="12" :xs="12">
                        <a-statistic title="今日新学" :value="todayReciteAmount + '/' + todayWillReciteAmount"></a-statistic>
                    </a-col>
                </a-row>
                <a-divider />
                <!-------------------------------------------------------------------------------->
                <a-spin :spinning="spinning_recite">
                    <a-row type="flex" justify="center">
                        <a-col :span="12">
                            <h1 :style="{ color: isForget ? 'red' : 'black'  }">{{ currentReciteMedicine.name }}</h1>
                            <span>{{ currentReciteMedicine.type + '/' + currentReciteMedicine.subType }}</span>
                        </a-col>
                    </a-row>
                    <a-divider />
                    <div v-show="isShowMedicineDetail">
                        <a-row type="flex" justify="center" :gutter="32">
                            <a-col :md="8" :sm="12" :xs="24">
                                <a-card title="性味" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                    <p class="card-text">
                                        {{ currentReciteMedicine.flavor }}
                                    </p>
                                </a-card>
                            </a-col>
                            <a-col :md="8" :sm="12" :xs="24" :gutter="32">
                                <a-card title="归经" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                    <p class="card-text">
                                        {{ currentReciteMedicine.channel }}
                                    </p>
                                </a-card>
                            </a-col>
                        </a-row>
                        <a-divider />
                        <a-row type="flex" justify="center" :gutter="32">
                            <a-col :md="8" :sm="12" :xs="24">
                                <a-card title="功效" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                    <p class="card-text">
                                        {{ currentReciteMedicine.function }}
                                    </p>
                                </a-card>
                            </a-col>
                            <a-col :md="8" :sm="12" :xs="24">
                                <a-card title="应用" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                    <p class="card-text">
                                        {{ currentReciteMedicine.application }}
                                    </p>
                                </a-card>
                            </a-col>
                        </a-row>
                        <a-divider />
                        <a-row type="flex" justify="center" :gutter="32">
                            <a-col :md="8" :sm="12" :xs="24">
                                <a-card title="重点" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                    <p class="card-text">
                                        {{ currentReciteMedicine.highlight }}
                                    </p>
                                </a-card>
                            </a-col>
                            <a-col :md="8" :sm="12" :xs="24">
                                <a-card title="毒性" :headStyle="{ 'font-weight': 'bold', 'font-size': '24px', 'color': 'green' }">
                                    <p class="card-text">
                                        {{ currentReciteMedicine.toxicity }}
                                    </p>
                                </a-card>
                            </a-col>
                        </a-row>
                        <a-divider />
                    </div>
                    <a-row v-show="!isShowMedicineDetail" type="flex" justify="center" :gutter="32">
                        <a-col :md="8" :sm="12" :xs="24">
                            <a-button type="primary" @click="remember()" style="width: 100%">记住了</a-button>
                        </a-col>
                        <a-col :md="8" :sm="12" :xs="24">
                            <a-button type="danger" @click="forget()" style="width: 100%">没记住</a-button>
                        </a-col>
                        <a-col :md="8" :sm="12" :xs="24">
                            <a-button type="dashed" @click="trash()" style="width: 100%">斩</a-button>
                        </a-col>
                    </a-row>
                    <a-row v-show="isRemember" :gutter="24">
                        <a-col :span="12">
                            <a-button type="danger" @click="forgetUndo()" style="width: 100%">没记住</a-button>
                        </a-col>
                        <a-col :span="12">
                            <a-button type="dash" @click="trashMore()" style="width: 100%">斩</a-button>
                        </a-col>
                    </a-row>
                    <a-divider v-show="isRemember" />
                    <a-row v-show="isTrash">
                        <a-col :span="24">
                            <a-button @click="restore()" style="width: 100%">恢复</a-button>
                        </a-col>
                    </a-row>
                    <a-divider v-show="isTrash" />
                    <a-row v-show="isShowMedicineDetail">
                        <a-col :span="24">
                            <a-button type="primary" @click="next()" style="width: 100%">下一个</a-button>
                        </a-col>
                    </a-row>
                </a-spin>
            </div>
            <div v-else-if="tabKey == 3">
                <a-result title="今日任务已全部完成！">
                    <template #icon>
                        <a-icon type="smile" theme="twoTone" />
                    </template>
                    <template #extra>
                        <a-button type="primary" @click="$router.push({ path: '/medicine/recite/log' })">去打卡</a-button>
                    </template>
                </a-result>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
        spinning_plan: false,
        spinning_recite: false,
        showSettingDrawer: false,
        form: this.$form.createForm(this),
        maxChapters: 0,
        allChapters: [{
            key: '解表药',
            title: ''
        }, {
            key: '清热药',
            title: ''
        }, {
            key: '泻下药',
            title: ''
        }, {
            key: '祛风湿药',
            title: ''
        }, {
            key: '化湿药',
            title: ''
        }, {
            key: '利水渗湿药',
            title: ''
        }, {
            key: '温里药',
            title: ''
        }, {
            key: '理气药',
            title: ''
        }, {
            key: '消食药',
            title: ''
        }, {
            key: '驱虫药',
            title: ''
        }, {
            key: '止血药',
            title: ''
        }, {
            key: '活血化瘀药',
            title: ''
        }, {
            key: '化痰止咳平喘药',
            title: ''
        }, {
            key: '安神药',
            title: ''
        }, {
            key: '平肝息风药',
            title: ''
        }, {
            key: '开窍药',
            title: ''
        }, {
            key: '补虚药',
            title: ''
        }, {
            key: '收涩药',
            title: ''
        }, {
            key: '涌吐药',
            title: ''
        }, {
            key: '攻毒杀虫止痒药',
            title: ''
        }, {
            key: '拨毒化腐生肌药',
            title: ''
        }],
        targetChapters: [],
        reciteMedicine: [],
        isShowMedicineDetail: false,
        todayReciteAmount: 0,
        todayReviewAmount: 0,
        currentReciteMedicine: null,
        isForget: false,
        isRemember: false,
        isTrash: false
    }
  },
  async asyncData({ $axios }) {
    let allMedicine = []
    let tabKey = 0
    let reciteSetting = null
    let todayWillReciteAmount = 0
    let todayWillReviewAmount = 0

    await $axios.get('IsSetMedicineReciteSetting')
    .then((response) => {
        if (response.data.code == 200) {
            if (response.data.status == 'false') {
                tabKey = 0
            }
            else if (response.data.status == 'true') {
                tabKey = 1
                reciteSetting = response.data.data
                todayWillReciteAmount = reciteSetting.todayWillReciteAmount
                todayWillReviewAmount = reciteSetting.todayWillReviewAmount
            }
        }
    })

    return {
        allMedicine: allMedicine,
        tabKey: tabKey,
        reciteSetting: reciteSetting,
        todayWillReciteAmount: todayWillReciteAmount,
        todayWillReviewAmount: todayWillReviewAmount
    }
  },
  methods: {
      changeChapter(nextTargetKeys, direction, moveKeys) {
          this.targetChapters = nextTargetKeys

          this.$axios.get('getNumMedicine', {
              params: {
                  chapters: this.targetChapters
              }
          })
          .then((response) => {
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.maxChapters = response.data.data
              }
          })
      },
      validatorTransfer(rule, value, callback) {
          if (this.targetChapters.length == 0) {
              callback('请至少选择一个子章节')
          }
          callback()
      },
      changePlan() {
          this.spinning_plan = true
          this.showSettingDrawer = true
          this.$axios.get('getPlanChapters_Medicine')
          .then((response) => {
              this.spinning_plan = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.targetChapters = response.data.data.chapters
                  this.maxChapters = response.data.data.maxChapters
                  this.form.setFieldsValue({ 'amount': response.data.data.currentAmount })
                  this.form.setFieldsValue({ 'isRandom': response.data.data.isRandom })
              }
          })
      },
      submit(e) {
          e.preventDefault()
          this.form.validateFields((err, values) => {
              if (!err) {
                  if (this.userBaseInfo.id == -1) {
                      this.$message.warning('先登录吧～')
                  }
                  else {
                      this.spinning_plan = true
                      this.$axios.post('submitReciteSetting_Medicine', qs.stringify({
                          chapters: this.targetChapters,
                          amount: this.form.getFieldValue('amount'),
                          isRandom: this.form.getFieldValue('isRandom')
                      }, { arrayFormat: 'brackets' }))
                      .then((response) => {
                          this.spinning_plan = false
                          if (response.data.code == 200 && response.data.status == 'success') {
                              this.$message.success('计划设定成功')
                              this.showSettingDrawer = false
                              this.$axios.get('IsSetMedicineReciteSetting')
                              .then((response) => {
                                  if (response.data.code == 200 && response.data.status == 'true') {
                                      this.tabKey = 1
                                      this.reciteSetting = response.data.data
                                      this.todayWillReciteAmount = this.reciteSetting.todayWillReciteAmount
                                      this.todayWillReviewAmount = this.reciteSetting.todayWillReviewAmount
                                  }
                              })
                          }
                      })
                  }
              }
          })
      },
      start() {
          this.spinning_recite = true
          this.$axios.get('getReciteMedicine')
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200) {
                  if (response.data.status == 'success') {
                      this.reciteMedicine = response.data.bank
                      // All done
                      if (this.reciteMedicine.length == 0) {
                          this.tabKey = 3
                      }
                      else {
                          this.currentReciteMedicine = this.reciteMedicine[0]
                          this.todayReciteAmount = response.data.todayReciteAmount
                          this.todayReviewAmount = response.data.todayReviewAmount
                          this.tabKey = 2
                      }
                  }
                  else if (response.data.status == 'nextDay') {
                      this.tabKey = 1
                  }
              }
          })          
      },
      remember() {
          this.spinning_recite = true
          this.$axios.post('recite_remember_medicine', qs.stringify({
              name: this.currentReciteMedicine.name,
              isReview: this.currentReciteMedicine.isReview
          }))
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.isShowMedicineDetail = true
                  this.isRemember = true
                  if (this.currentReciteMedicine.isReview) {
                      this.todayReviewAmount += 1
                  }
                  else {
                      this.todayReciteAmount += 1
                  }
              }
          })
      },
      forget() {
          this.spinning_recite = true
          this.$axios.post('recite_forget_medicine', qs.stringify({
              name: this.currentReciteMedicine.name,
              isReview: this.currentReciteMedicine.isReview
          }))
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.isShowMedicineDetail = true
                  this.isForget = true
                  if (!this.currentReciteMedicine.isReview) {
                      this.todayReciteAmount += 1
                      this.todayWillReviewAmount += 1
                  }
              }
          })
      },
      forgetUndo() {
          this.spinning_recite = true
          this.$axios.post('recite_forgetUndo_medicine', qs.stringify({
              name: this.currentReciteMedicine.name,
              isReview: this.currentReciteMedicine.isReview
          }))
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  if (this.currentReciteMedicine.isReview) {
                      this.todayReviewAmount -= 1
                  }
                  else {
                      this.todayWillReviewAmount += 1
                  }
                  this.next()
              }
          })
      },
      trash() {
          this.spinning_recite = true
          this.$axios.post('recite_trash_medicine', qs.stringify({
              name: this.currentReciteMedicine.name,
              isReview: this.currentReciteMedicine.isReview
          }))
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  this.isTrash = true
                  this.isShowMedicineDetail = true
                  if (this.currentReciteMedicine.isReview) {
                      this.todayReviewAmount += 1
                  }
                  else {
                      this.todayReciteAmount += 1
                  }
              }
          })
      },
      trashMore() {
          this.spinning_recite = true
          this.$axios.post('recite_trashMore_medicine', qs.stringify({
              name: this.currentReciteMedicine.name
          }))
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  if (this.currentReciteMedicine.isReview) {
                      this.todayReviewAmount += 1
                  }
                  else {
                      this.todayReciteAmount += 1
                  }
                  this.next()
              }
          })
      },
      restore() {
          this.spinning_recite = true
          this.$axios.post('recite_restore_medicine', qs.stringify({
              name: this.currentReciteMedicine.name,
              isReview: this.currentReciteMedicine.isReview
          }))
          .then((response) => {
              this.spinning_recite = false
              if (response.data.code == 200 && response.data.status == 'success') {
                  if (this.currentReciteMedicine.isReview) {
                      this.todayReviewAmount -= 1
                  }
                  else {
                      this.todayReciteAmount -= 1
                  }
                  this.next()
              }
          })
      },
      next() {
          this.isForget = false
          this.isRemember = false
          this.isTrash = false
          this.isShowMedicineDetail = false
          this.reciteMedicine.shift()
          // Next bunch
          if (this.reciteMedicine.length == 0) {
              this.start()
          }
          else {
              this.currentReciteMedicine = this.reciteMedicine[0]
          }
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
    text-decoration: none;
}

.card-text{
    font-size: 18px;
}
</style>
