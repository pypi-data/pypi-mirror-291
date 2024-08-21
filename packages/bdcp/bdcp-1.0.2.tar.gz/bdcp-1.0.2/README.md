## 简介

bdc是一个竞赛辅助工具

## 使用方法

1、引入包

```
import bdcp
```

2、获取数据

```
bc = bdcp.connect(username, password, module_id)
```

3、基本内容设置

```
bc.setbasic()
```

4、获取check

```
bc.get_check(hostname)
```

5、获取文档

```
bc.get_element_detail(element_id)
```

6、获取abcd

```
bc.get_abcd("")
```

