export const state = () => ({
  // baseUrl: 'http://localhost:8000',
  baseUrl: '',
  classes: [{
    value: 'zhongyi',
    label: '中医学院',
    children: [{
      value: 'wuyi',
      label: '五年制一班',
    },
    {
        value: 'wuer',
        label: '五年制二班',
      }],
  }]
})
