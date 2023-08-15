// 网创平台课程返回数据解密分析 https://jiucai.trwwhii.top/#/pages/detail/detail?id=13307
const CryptoJs = require("crypto-js");
const Md5Crypto = require("crypto");
const AesKey = "01021f7358f7ed6ef5b8d530391d223b";

function GetKey(e){
    for (var n = [], a = 0, i = e.length; a < i / 16; a++) {
        var r = e.slice(16 * a, 16 * (a + 1));
        n.push(r)
    }
    return n
}

var GetHeaderTimeStamp = function(source) {
    keys = GetKey(AesKey)
    let password = CryptoJs.enc.Utf8.parse(source)
    let key = CryptoJs.enc.Utf8.parse(keys[0])
    let iv = CryptoJs.enc.Utf8.parse(keys[1])

    cfg = {
    mode:CryptoJs.mode.CBC,
    padding:CryptoJs.pad.Pkcs7,
    iv:iv
    }

    let encSource = CryptoJs.AES.encrypt(password,key,cfg).toString();
    return encSource
}


var AesDecryptData = function(source,timestamp){
    let obj = Md5Crypto.createHash("md5");
    datakeys = GetKey(obj.update(timestamp + AesKey).digest("hex"))
    let key = CryptoJs.enc.Utf8.parse(datakeys[0])
    let iv = CryptoJs.enc.Utf8.parse(datakeys[1])
    cfg = {
        mode:CryptoJs.mode.CBC,
        padding:CryptoJs.pad.Pkcs7,
        iv:iv
    }

    let decSource = CryptoJs.AES.decrypt(source,key,cfg).toString(CryptoJs.enc.Utf8);
    return decSource
}

// let s = `Tfpdcxn5hmX9iulPA9tlR5SBsZuYUbGJd6SMoPAO1tR76B7+TcBgFLZNGgEvqKmd/m44lSi6Aq6mHw+PXiTz0iFLGIl6oZzFK8cmWIh6Xie6s958Jq2AChy5okwrbZ9n2g9ZZHvqsefMhZy8mYUZK/3MEqF38tzeAh85paNQktQ6VV/V04GHNQITTyJPK7XxXdwFtUW29gRsuEEeZ00OCTTcZG0iPSDFaBeorqTghuBbNekpJ/xJ6TMBsdF/sTtInK+HiIMUIUb5ZaKEiixPl/aDSWy6DqUk1ttQyx21bYRZtQnoqgDlthRPHk0y5nAvq2Al+sXDzwekKiNG2Xlx8Jz4jwWIIeq9jLuxItAgt4My+idE0KkpvgUCKbJ6Emyrfj0EZrvmgMZDu7SO4uaa8OwGKgZokqATpO/LwBnb5BXfm7tS+OsSXCfRYnNQpQt12G3+R2yI8nzv6aiukT1+VpqOBKYkC1+Wjeu4iqlL9XL8rcFSUn4xZGksv5/s+w/CCdU/JdqvGyQWOce08W0jdIFURs9teMLd1F0W8g4DIeMDIGXAKXVUoFxCxRwZdgDU717hFFKDzoHzPfWyAZWF5VPP832w/a72WlyepKBD+c7S8fpcmFtgvwXYcsSvpJGRhNiYIS6YfjcpT/03AYUu8UXQqgIxRwq4pBvZfMLQBy2/eQxKQR2ChFQlkO6IGS/VFfr0XuWFBzxE4Qb66gyzNyBIUJDCFOI2ctmiLHmMH+sjD/rV8XogAmRa8nLOBuC5ahHUfZTnQk/AU/h1sOV6WZUgezFembBrfkkq59acnPVF+cnNr1meU+SXp6wuEkdik5gCI/KWeq+569mnd5ho94giLN2YSpgjgoAB6oxmjCHGtq6qgOSAjKEqJTMSqqD7BS3pjqfqPT8LISlqacKd3PF9vc6QeMsi5L1AD+WO17GiZqgju70BnH1taw1YNCkVrvDDuzwrN27S0EM6jQzmJhUeyA5Xy5LDw2ciZ/2Dze4G7UTT2I/O0HkRkd5c3fXzykxOpEJl1f8inekRmnQDBB+/ObLzhK+byvDdrsjg1InZR5eMmoMqQQqSm+Vz/SetJB+TXDVEBxZTimJ4NVy3teBO+bGGBw8EihelHG74b5G34ltQWQd/dxUX5iLLLAx2b5hpVuChFlu180ZVYGWCiRTh3wo/sC3F/N6p/vET2sqM1QzvVLMymSdXmwadVzNKFtnFDesiBGipeU3phO7nYMoD+WRXTvGKwVCi23KfBIlrbWVvryIWB79wPsp9fBDfqOxCkMkdR58ZTkLSkHWf8163cJjEiTmRCtHSaoYmqrTjZh5dEgw2PQbOC+lxHpY8U6l6XHqRtv769c0mg691ev+7VmYwSSGcC9fcBF7HLywXUHDTwjh3OQKE1BvT7bUvpS0FE5McPAwQmT6EThvd53EgQtUJ2KSk+ad0ZNKcp5liCwG/zz9y+cl9B1iIygjSlbWjxgzFQhykl9lYrYSBk3Oj1+kuaUa5I0WLb+cmI7LjfQ/kR4rLT+bu2ulQOIE5QWnqiwi7XHIQehGsXisbK5osI/N72HJLXXSc4XlfAUMLcDqgS6+DKcI3nbzTU5MBNv0rCUgUliiC0sHOnTmg1hwVMHlWIlRj8Wnb9SgelsnYY8eTAbmVaIi9HN15LFRIkFDy8k8lzoakgJijB2xARcc1Oax6iAWNfgtXCUlFtMbVlgzGixQnFNQTJdthlURvBGWhoHfrBpeQc+X7fKae5Y7GFP93ABYI7iVO04aUpXntGE0SZkMNLNhzHMuTt7uD3vg1tKxiXJLjxVZO2Tf3MgpdoMP8L8O98QOz2RG2wZ8e8L+8AitjGBCWS4DxZPESjdRE9jFxP8C/bQoUcbOH/x+qIIIe6tqOF2YvFIZeW1tIFNl5QlrO70SvDsDaHqdKoy5Pgz94cxm4TSy2vN5zs0cXcG2FiyDm38GBYIEutTnTO/KqhPKX82IGYxhiROHWtxL/hABXaEr5PNKyMA5b1S0IpZ8i5AK05c/9IJp9L8PEZwgdFKLIn3MEXOvZX1L4/YKm5ulxhXDX/AyzhNoXoJOMttMABZ/Muo2Rky2iZhAfg3PwE8A+H7PwBd1nC5f+tT4zgn18mmrU8oehw0Rugn7se7n5hRmCCSd/JzjVJikqu0/uYvogcHofM8XDfzQw4W0Rlpyd+PLJoMdMHHU5Z8Kj/Tbv0Yfpz38ZRnVEwzVWRpcYxQ+uub4+n9V2Vz8hm41gsDrEPMzhRBTmXkd1oo/zTtavn+F2fwgzkSqbfpdOUDrprYBAaOBEcZdnAJGKQMdI5a99/uI/Pho8o7jNNmQ8leFmMGEaCPJ/Hjd6VXiVG1Wst3bLnBhfPgRvREKPZ2ZNgjavapdZRfJJ1c5hRv33QNLBLKtV3HuDXU/Y7adziaoWMOPC7ZP25M81u8dzB79E14zvW0V3eE6vAPZTnWe50pzCV3nG7KzbVOrBJNChb9sXuDIZZn6jEPjmvW4pxJvzGeG1CcQ35iWAq8PkaYtHP54aA7rSrQgloFIB4GSdqyUPzyNhq32ArQB3fgSy7gg+RbVPQufD7oEsmFuk0BEdcn1tSZ4VLwZzMT32FsQmkm1ZBWmFD12y8j3I+wKflsEB9H0JZYdHPZI5xeJg63gxxcMopyN+D7dxfknKzBF4rZEaWGBT0UTMZvHuURFdOHEF5GgGsNGmLR3ENHeCv4b9wXD8/qa3E2Ckx66G0nOGO8FK0nC/6HKE2fHgkDF5jxKvSfht0vdF3X0x9mjoEqdpszsN3sTjIt7iM8dumf9recHmZ0AWU1kaRcgjEpkkGLifdCSxHFnvO+w9bygRo8QkSAGB/LH7DqaWO2XGXeM2PbTXqhxevmKJTN9Arv3CUNThtskRDKlx2aefUwRPRl4UlPjWTkjuSO7FImI+6iZTgtmag3ZcYrUZfV1L31Jr+WqVrN6dVAVe0yapnne46vC/rBsCpY1rfVVtJZXvnwDLkPh8XHRHVgzqit9uhXXHaGDBphEfmndJAAxSySaoR2A5NXMayk67VBKateyC91B0jLR20XUT1cmZlcLPzWabHxbVM7XK+2COLb4SwFSnRzaJ8CBeTP0xUDUuCSVIp+j2xpxygyxnk+bSgSC7JVOle9Q+q9OrIoyNALatxmEBAFw4uWrc9qR5meidWYO2J/LD8IIWRMm1+8dMfrTDNN4OXH0jUFRAuiHuvRoXJg4ncY8OIsJ+ydmdIq0x8blTpqDl+KWdm/OubRXZQIi0RyDIQYy+nG9xauHLx1f+ydrQjji8p7HNV+dw2s6xJzQ34UToenRebP45vYt4m7ibQ2X/gV9RZx6lPKowW8IS2sYBMZAExxXg7y8QKKPPi5Jx3F/mK0csWK268ZJv/rSWBVdy/Q+oZ4s9f/RrW4B9kgeujNCjDYlgkr7KSubOEjPtxnj4wzw87YdoaVk39nKuc4HlDqU2AW+dZ0056YIB1MX8s5XIUGTRvD0Maa/P/fJeXa45b2fHndXaMhEnEL/cpk6uMcDLsG/kRPMMrfKH3O7iBw31XpH486MZybgdKoy9ja+Ol0Dk0SJ8ENE9iIKSnORfTV6AkP5QmgEL8Dy/G/kzVut7LK6P9pFa/1qXtlG11UHU8Tt6pqOi4q0D6DFi411E+w4jaHBdT6Jquh/iQluw8Ee0kkyo5sj3xiV1PJRtrlj+frEBvg3fkzylvVzhDLsl5AacYEW99HVO2qaH1hxnSPDuXzDMjngI4OUpjlgSXrrq8iH6a6RhW2HO1z505hmy0Eqy++Xd+GBJ9S01SxtyDVTJ5sQY7JAc2z7hWrhf7KaTsP3WjyaR4IQ8MKV0CKepCmsu+pijTjsgHCjnCBSl2cC7N3URo70vx87BMc6Dq7cr0HdV6p/J8BEqM35xPIHzkegqW1fQqaavP2MMw7CWX0HgzzLGyIaHj4i5zuu0iglJ9wH9GrnveAB+krAVjuK9rDsnlTE7g5+Gw41lcOHi+3MbySzSV72oXCGSE0jYU4zzClfxMq5pO8N2sUtM2TLEuyhKe6xr0iV7WZDVY0airK4btuMqH0QgwVXs3jO6of96WEHVRH9jkP6Qg4maDsZpadiPKYLIt9ESru/frkENPxOnR/aTms4BDlnyTL6+ukUHSpdzQDHzMYJ+AwO2n2dIB0iVz7kanguQQgK1qcu18s1HwwHI82IUuQgl1lWIzp6Am8m8ZvAjxc6+ZhfG8ndHJ7L4jkdUSzZQWdurFuo0zH3F3cj9Thx7KirQO5hoX2HSLqX5vTwvLxTmn68xxXBpAFuWCYTj9US8tVPE2BAngNHWYxHjPVuiN0Lg/ZpQchC7CMdRlBqjxal6Y5lXgH8Sl5hIp2mqz+N5kd0YchBckgSkOY2b2VXgDuBrsCHyh+kaiT5IIw7DFYZrcZcWRuxhj3XWbvNGTjOxbwI2/RBh1mKqzALjnokp/G8HCT9YYl6IlUlO3zKYvKf1NJe1xjtadMhxBoxcwn+bCFjtyAZBGqqqHMuMeHdT0quNAn3OpeCPONIxsBfjgWis/QStMXB0ORSkpZv2/oVFkFrSdtmUrtXd4OPlmR0Zl1ZLF3MPfr8jFNtrXeNT4frrEL3e7Liks6cKB0vXcO5ZqezZWDl6s+bHPUTs8nunJi0TdDCX/B4in69IRg2cwaHDdajvYexffDaU/MgrwaxjW4dkKTQycQxg0aoTlQPX/Nw3L11l0ECk//hGnvBNrYn9PnVAwdMPoFbHRzlkBxYyjNF87gVmie3uaaZyFhcvAkaJdaJ9vm1zCNJ2OECY1m4hqkK7bW9TTWSghIjoTxAkk/xCqo98pH7ywHwhkjXFHIPKvtfu4uBwy3W7Z6nIOzY+sdKCbk66uoYHvkn042tT6qkPX4g+XJhh/1RCo8ENIMbqkGCdMdnZ6LvPjB9q4sWGUY1Kkk8lU+ndFoHev5R6m8V/6TmuX55ApYJ8x7kgL5ld2HSrINaaoq8ROs7Zv8oBanHoHCtjSZeNDHxGUoVL5USyWAvnO9sh96IfYrx7jlnh/HfYLmr7qrfvJZUjusinLeuEGIKCPGCjvwWi/iwrx9TAwrH0egq5ZU38IHtIjUh947eqBoV1QroGTWyuKpbh2+EHQs+hEzARaCH5TDGGifWJe9atFrc+0vY2ZmW+zAVg5A2kxBVVfQjUtlqObjX8gZccr4RrAqRmG79ogljxj+TpEFnxJOMDkqq9goQLhx0E4+wW4BDsR0HJni1N7wSQ+HA+DCzITrDFCLeKfanUsSz6UPENMhlY4ViI359G8Zgf6KNczFplcTnUB3GDxInxcAcmuMiZ6aCyvbiIpb+mS63C+8j/f3GCbc5ID+dVdbUcIgaA/jK+52c2hEp3MFgqZDceubWX7KZgHxFMKoZsqv9f47N3nhE5vyFDMcUtM59v78MbVybvz3vuKO23Uc80xGSDzvQxOxrdvLizqsBsMf19SUAzxJjW4zVKn9cTHsPxzJGvi5calXpE0nWg685tyo8trtN4hToIE1ZV4B5EU+yZtOj69DoRwJo2g0DZg4nI7JoVDuQHX3O3GF0s2K6id3FHWaK4JRcKqrkxgaElCGwbTGYXUnLcTf89/cMDMSpHIuPuWV3l3lV8Fpkzq2KfYL1Hcn3EXddJX1CeRj3qSzSHjN7/wyRoWxJEO/EsZ0O3OZqrRugDIWOk1XJTC5ibhRJKWmA1x0O4ivUfUR1Gs02w5tw7OA==`
// let dec = AesDecryptData(s,1691207830)
// console.log(dec)


// export GetKey

module.exports.GetHeaderTimeStamp = GetHeaderTimeStamp;
module.exports.AesDecryptData = AesDecryptData;