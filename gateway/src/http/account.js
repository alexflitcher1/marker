import {$authHost, $host, $refreshHost} from './index'

export const signup = async (user) => {
    const data = {
        firstName: user.firstName,
        lastName: user.lastName,
        login: user.login,
        email: user.email,
        password: user.password
    }
    const response = await $host.post('/account/mail', data)
    return response
}

export const create = async (user, mail) => {
    const data = {
        user: {
            firstName: user.firstName,
            lastName: user.lastName,
            login: user.login,
            email: user.email,
            password: user.password
        },
        mail: {
            email: mail.email,
            code: mail.code
        }
    }
    const response = await $host.post('/account/create', data)
    return response
}

export const token = async (login, password) => {
    const response = await $host.post('/account/token', {login, password})
    return response
}

export const refresh = async () => {
    const response = await $refreshHost.post('/account/refresh')
    return response
}

export const userStatus = async () => {
    const response = await $authHost.get('/account/status')
    return response
}

export const userSettings = async () => {
    const response = await $authHost.get('/account/settings')
    return response
}