export const state = () => ({
    timer: null,
    questions: [],
    banks: [{
        key: '中医基础理论',
        subBanks: [{
            key: 'zyjcll-1',
            title: '第一章'
        },
        {
            key: 'zyjcll-2',
            title: '第二章'
        }]
    }]
})

export const getters = {
    getSubBanks: (state) => (bank) => {
        return state.banks.filter((subBank) => {
            return subBank.key == bank
        })[0].subBanks
    }
}

export const mutations = {
    setQuestions(state, questions) {
        state.questions = questions
    },
    setTimer(state, timer) {
        state.timer = timer
    }
}

export const actions = {
    setBank({ commit }, { questions, timer }) {
        commit('setQuestions', questions)
        commit('setTimer', timer)
    },
}
