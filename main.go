package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
)

func crawlList() {
	client := &http.Client{}
	var data = strings.NewReader(`cid=3&page=2&kw=`)
	req, err := http.NewRequest("POST", "https://jiucai.trwwhii.top/baseurl/api/public/?s=App.Tools.Index", data)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("authority", "jiucai.trwwhii.top")
	req.Header.Set("accept", "*/*")
	req.Header.Set("accept-language", "zh-CN,zh;q=0.9")
	req.Header.Set("content-type", "application/x-www-form-urlencoded")
	req.Header.Set("cookie", "PHPSESSID=kj3i6k8heitbtaotk0tr5pci51; SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1")
	req.Header.Set("mysid", "uZkyzncGNnyVgi1iiCJczZpJsoX7DGKQ")
	req.Header.Set("origin", "https://jiucai.trwwhii.top")
	req.Header.Set("referer", "https://jiucai.trwwhii.top/")
	req.Header.Set("sec-ch-ua-mobile", "?0")
	req.Header.Set("sec-fetch-dest", "empty")
	req.Header.Set("sec-fetch-mode", "cors")
	req.Header.Set("sec-fetch-site", "same-origin")
	req.Header.Set("timestamp", "tyeVmHWhI/asq7KYWwcoTQ==")
	req.Header.Set("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	bodyText, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s\n", string(bodyText))
}

func main() {
	crawlList()
}
