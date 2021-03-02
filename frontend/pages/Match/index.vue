<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>比赛动态</h1>
                            <p class="subheading">参加比赛拿学分～</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px" />
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <a-table :columns="columns" :dataSource="matchList" rowKey="id">
                        <a slot="_title" slot-scope="title, record" @click="matchDetail(record.id)">{{ title }}</a>
                        <span slot="startDate" slot-scope="startDate">{{ moment(startDate).format('lll') }}</span>
                        <span slot="endDate" slot-scope="endDate">{{ moment(endDate).format('lll') }}</span>
                        <template slot="state" slot-scope="state">
                            <a-tag v-if="state == '未开始'">{{ state }}</a-tag>
                            <a-tag v-else-if="state == '进行中'" color="green">{{ state }}</a-tag>
                            <a-tag v-else-if="state == '已结束'" color="red">{{ state }}</a-tag>
                        </template>
                    </a-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
        moment,

        visible: false,
        lecturerInfo: '',
        columns: [{
            dataIndex: 'title',
            title: '标题',
            scopedSlots: { customRender: '_title' }
        }, {
            dataIndex: 'totalBonus',
            title: '总奖金(元)',
            sorter: (a, b) => a.totalBonus - b.totalBonus,
        }, {
            dataIndex: 'startDate',
            title: '开始时间',
            scopedSlots: { customRender: 'startDate' }
        }, {
            dataIndex: 'endDate',
            title: '结束时间',
            scopedSlots: { customRender: 'endDate' }
        }, {
            dataIndex: 'state',
            title: '状态',
            scopedSlots: { customRender: 'state' }
        }]
    }
  },
  async asyncData({ $axios }) {
    let matchList = []

    await $axios.get('getMatchList')
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            matchList = response.data.data
        }
    })

    return {
        matchList: matchList
    }
  },
  methods: {
      matchDetail(id) {
          let routeData = this.$router.resolve({ path: '/match/detail', query: { id: id } })
          window.open(routeData.href, '_blank');
      }
  },
  computed: mapState({
      baseUrl: state => state.baseUrl
  })
}
</script>

<style scoped>
a {
    text-decoration: none;
}
</style>
