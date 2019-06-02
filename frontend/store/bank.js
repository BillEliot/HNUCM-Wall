export const state = () => ({
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
    setBank({ commit }, questions, timer) {
        commit('setQuestions', questions)
        commit('setTimer', timer)
    }
}
