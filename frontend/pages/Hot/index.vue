<template>
    <div>
        <!-- banner -->
        <div class="main-wrapper">
            <div class="page-title">
                <div class="container">
                    <div class="title-holder">
                        <div class="title-text text-center">
                            <h1>校园热点</h1>
                            <p class="subheading">掌握前沿咨询</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="margin-top: 50px"></div>
        <!-- container -->
        <div class="container">
            <div class="row">
                <div class="col-md-12 col-sm-12">
                    <a-table :columns="columns" :dataSource="hotList" rowKey="title">
                        <router-link slot="_title" slot-scope="text, record" :to="{ path: '/hot/detail', query: { id: record.id }}">
                            {{ text }}
                        </router-link>
                        <a-tag slot="type" slot-scope="text">{{ text }}</a-tag>
                        <!-- search -->
                        <div
                            slot="filterDropdown"
                            slot-scope="{ setSelectedKeys, selectedKeys, confirm, clearFilters, column }"
                            style="padding: 8px"
                        >
                            <a-input
                                v-ant-ref="c => (searchInput = c)"
                                :placeholder="`搜索 ${column.dataIndex}`"
                                :value="selectedKeys[0]"
                                style="width: 188px; margin-bottom: 8px; display: block;"
                                @change="e => setSelectedKeys(e.target.value ? [e.target.value] : [])"
                                @pressEnter="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
                            />
                            <a-button
                                type="primary"
                                icon="search"
                                size="small"
                                style="width: 90px; margin-right: 8px"
                                @click="() => handleSearch(selectedKeys, confirm, column.dataIndex)"
                            >
                                搜索
                            </a-button>
                            <a-button size="small" style="width: 90px" @click="() => handleReset(clearFilters)">
                                重置
                            </a-button>
                        </div>
                        <a-icon
                            slot="filterIcon"
                            slot-scope="filtered"
                            type="search"
                            :style="{ color: filtered ? '#108ee9' : undefined }"
                        />
                        <template slot="customRender" slot-scope="text, record, index, column">
                            <span v-if="searchText && searchedColumn === column.dataIndex">
                                <template
                                    v-for="(fragment, i) in text
                                        .toString()
                                        .split(new RegExp(`(?<=${searchText})|(?=${searchText})`, 'i'))"
                                >
                                    <mark
                                        v-if="fragment.toLowerCase() === searchText.toLowerCase()"
                                        :key="i"
                                        class="highlight"
                                    >
                                        {{ fragment }}
                                    </mark>
                                    <template v-else>{{ fragment }}</template>
                                </template>
                            </span>
                            <template v-else>
                                {{ text }}
                            </template>
                        </template>
                    </a-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import qs from 'qs'
import moment from 'moment'
import { mapState } from 'vuex'

export default {
  layout: 'common',
  data() {
    return {
        moment,

        searchText: '',
        columns: [{
            dataIndex: 'title',
            title: '标题',
            scopedSlots: { customRender: '_title' },
            scopedSlots: {
                filterDropdown: 'filterDropdown',
                filterIcon: 'filterIcon',
                customRender: 'customRender',
            },
            onFilter: (value, record) => record.title.toString().toLowerCase().includes(value.toLowerCase()),
            onFilterDropdownVisibleChange: visible => {
                if (visible) {
                    setTimeout(() => {
                        this.searchInput.focus()
                    }, 0)
                }
            }
        }, {
            dataIndex: 'date',
            title: '日期',
            sorter: (a, b) => {
                if (moment(a.date).isAfter(moment(b.date))) return 1
                else if (moment(a.date).isBefore(moment(b.date))) return -1
                else return 0
            }
        }, {
            dataIndex: '_type',
            title: '类型',
            scopedSlots: { customRender: 'type' },
            filters: [
                { text: '新闻', value: '新闻' },
                { text: '通知', value: '通知' },
                { text: '招标公告', value: '招标公告' },
                { text: '中标公告', value: '中标公告' },
                { text: '瓜', value: '瓜' },
            ],
            onFilter: (value, record) => record._type.includes(value)
        }]
    }
  },
  async asyncData({ $axios }) {
    let hotList = []

    await $axios.get('getHotList')
    .then((response) => {
        if (response.data.code == 200 && response.data.status == 'success') {
            hotList = response.data.data
        }
    })

    return {
        hotList: hotList
    }
  },
  methods: {
      handleSearch(selectedKeys, confirm, dataIndex) {
          confirm()
          this.searchText = selectedKeys[0]
          this.searchedColumn = dataIndex
      },
      handleReset(clearFilters) {
          clearFilters()
          this.searchText = ''
      },
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
