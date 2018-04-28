// ==UserScript==
// @icon            http://weibo.com/favicon.ico
// @name            ΢����Ƶ��������
// @namespace       http://weibo.com
// @author          ����ؼֹ��
// @description     ����΢����Ƶ
// @match           *://weibo.com/tv/v/*
// @require         http://cdn.bootcss.com/jquery/1.8.3/jquery.min.js
// @version         0.0.1
// @grant           GM_addStyle
// ==/UserScript==
(function () {
    'use strict';
    //��Ԫ���ݿ��е�@grantֵ���Ӧ������������һ��style��ʽ
    GM_addStyle('#down_video_btn{color:#fa7d3c;}');
    //��Ƶ���ذ�ť��html����
    var down_btn_html = '<li>';
    down_btn_html += '<a href="javascript:void(0);" id="down_video_btn" class="S_txt2" title="��Ƶ����">';
    down_btn_html += '<span class="pos">';
    down_btn_html += '<span class="line S_line1" node-type="comment_btn_text">';
    down_btn_html += '<span>';
    down_btn_html += '<em class="W_ficon ficon_video_v2 S_ficon">i</em>';
    down_btn_html += '<em>��Ƶ����</em>';
    down_btn_html += '</span>';
    down_btn_html += '</span>';
    down_btn_html += '</span>';
    down_btn_html += ' <span class="arrow"><span class="W_arrow_bor W_arrow_bor_t"><i class="S_line1"></i><em class="S_bg1_br"></em></span></span>';
    down_btn_html += ' </li>';
    //������ƴ�ӵ�html������뵽��ҳ���ul��ǩ��
    var ul_tag = $("div.WB_handle>ul");
    if (ul_tag) {
        ul_tag.removeClass("WB_row_r3").addClass("WB_row_r4").append(down_btn_html);
    }
    var videoTool = {
        //��ȡ�ļ���
        getFileName: function (url, rule_start, rule_end) {
            var start = url.lastIndexOf(rule_start) + 1;
            var end = url.lastIndexOf(rule_end);
            return url.substring(start, end);
        },
        //�������ؿ�
        download: function (videoUrl, name) {
            var content = "file content!";
            var data = new Blob([content], {
                type: "text/plain;charset=UTF-8"
            });
            var downloadUrl = window.URL.createObjectURL(data);
            var anchor = document.createElement("a");
            anchor.href = videoUrl;
            anchor.download = name;
            anchor.click();
            window.URL.revokeObjectURL(data);
        }
    };
    $(function () {
        //��ȡ��������video������
        var video = $("video");
        var video_url = null;
        if (video) {
            video_url = video.attr("src"); //��ȡ��Ƶ���ӵ�ַ
        }
        //ִ�����ذ�ť�ĵ����¼����������غ���
        $("#down_video_btn").click(function () {
            if (video_url) {
                videoTool.download(video_url, videoTool.getFileName(video_url, "/", "?"));
            }
        });
    });
})();