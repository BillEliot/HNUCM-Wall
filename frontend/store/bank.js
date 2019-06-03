export const state = () => ({
    questionType: ['单选-A型题', '单选-B型题', '多选', '填空', '判断', '问答'],
    timer: null,
    questions: []
})

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
    }
}
