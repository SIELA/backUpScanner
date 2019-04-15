# backUpScanner
Backup file scanner
备份文件扫描器/敏感文件扫描器cd backUpScanner

用法：  
<code>git clone https://github.com/SIELA/backUpScanner  </code>  
<code>cd backUpScanner</code>  
<code>python ./backUpScanner -h www.baidu.com</code>单个扫描    
<code>python ./backUpScanner -H targetfile.txt</code>批量扫描 

./suffixes.txt里面是要扫描的后缀  
./filenames.txt里面是要扫描的文件名  
可以自己定制需求，笛卡尔积数量  
程序会自动判断是域名还是ip，如果是域名自动取二级域名为文件名扫描所有后缀：  
www.baidu.com--->
scan:www.baidu.com/baidu.sql.....  
scan:www.baidu.com/baidu.bak.....   
....   
源码比较简(la)单(ji)，可以自己修改加入线程、队列、延时功能

