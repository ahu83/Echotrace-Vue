import request from '@/utils/http'

export function test(params) {
  return request({
    url: '/aa/bb',
    method: 'post',
    params: params
  })
}

