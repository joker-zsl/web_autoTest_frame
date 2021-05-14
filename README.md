# 项目简介

这是一个简易的web自动化测试框架。基于selenium和unittest开发，使用page object的设计模式，以关键字驱动用例执行。

# 项目结构

│  local_execute.py                                    ----本地调试用的文件
│  main.py                                                   ----主执行文件
│  README.md
│
├─drivers                                                     ----浏览器驱动放置的文件夹
│      chromedriver.exe
│
├─frame                                                      ----框架主体代码
│         config.py                                           ----框架配置文件
│  ├─core
│           basepage.py                                   ----基础关键字的封装
│           browser.py                                     ----控制浏览器
│           decorators.py                                 ----一些装饰器
│           driver.py                                          ----封装selenium的操作
│           errors.py                                          ----自定义错误
│           testcase.py                                      ----组装testcase的模板
│           testsuit.py                                       ----加载testsuit
│  │  ├─BeautifulReport
│                BeautifulReport.py                    ----报告输出
│                template.html                            ----报告模板
│  ├─utils
│           handle_excel.py                              ----操作excel
│           handle_log.py                                 ----日志
│           handle_path.py                              ----操作路径
├─pages
│       common_page.py                              ----用户自定义的page行为，可以自己封装关键字
│
├─reports                                                     ----报告文件夹（报告、日志、截图）
│  └─report_20210513                               ----报告按日期生成不同文件夹存放
│      │  20210513.log
│      │  report_20210513151800.html
│      └─screenshots
└─testcases                                                   ----测试用例文件夹
    │  ControlPanel.xlsx                                  ----控制用例执行的文件
    └─cases                                                      ----测试用例存放文件
            testcase.xlsx                                       ----用户用关键字拼装成的测试用例（测试流程）

# 项目使用

