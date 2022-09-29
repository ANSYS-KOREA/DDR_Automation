# Ansys DDR Eye Analyzer - ADEA v1.1



<!-- ![Main GUI](./Resources/fig/main_GUI.bmp) -->
<details>
<summary><span style="font-size:200%"> What's New? </span></summary>

<blockquote>

<details>
<summary><span style="font-size:200%"> v1.0.1 </span></summary>

>   #### The process for choosing a version of Ansys Electronics Desktop(AEDT) has been modified.
>   * ##### v1.0 : AEDT executes in a specific version with reference to environmental variables.
>   * ##### v1.0.1 : The version of AEDT can be selected using 'Version Selection' window.

</details><br>

<details>
<summary><span style="font-size:200%"> v1.1 </span></summary>

>   #### Exporting IBIS optimization results to an Excel report has been updated.

</details>

</blockquote>
</details>

---
<details>
<summary><span style="font-size:200%"> What's coming? </span></summary>

</details>

---
<details>
<summary><span style="font-size:200%"> What is ADEA? </span></summary>

>### A new Solution for DDR analysis by Ansys Korea.
>![ex_screenshot](./Resources/fig/ADEA_Intro.png)
</details>

---
<details>
<summary><span style="font-size:200%"> Why ADEA? </span></summary>

<blockquote>
<details>
<summary><span style="font-size:200%"> 1. Easy </span></summary>

>   * ### Pre-defined User Configurations
>   * ### Pre-defined DDR Specifications
>   * ### Automatic Net Classification & Target Net Assign Algorithm
>   * ### Selective Verification Process
>   ![ex_screenshot](./Resources/fig/easy.png)
</details>
</blockquote>

<blockquote>
<details>
<summary><span style="font-size:200%"> 2. Simple </span></summary>

>   * ### One-Click Verification Process
>   ![ex_screenshot](./Resources/fig/simple.png)
</details>
</blockquote>

<blockquote>
<details>
<summary><span style="font-size:200%"> 3. Customizable </span></summary>

>   * ### Customziable Verification Algorithm & Process
>   * ### Customziable Final Report (Excel, HTML, etc.)
>   ![ex_screenshot](./Resources/fig/customizable.png)
</details>
</blockquote>
</details>

---
<details>
<summary><span style="font-size:200%"> User Guide - PDF </span></summary>

> ### [Quick Guide (EN) - PDF](./Resources/help/Quick_Guide_EN.pdf)
> ### [User Guide (EN) - PDF](./Resources/help/User_Guide_EN.pdf)
> ### [Quick Guide (KO) - PDF](./Resources/help/Quick_Guide_KO.pdf)
> ### [User Guide (KO) - PDF](./Resources/help/User_Guide_KO.pdf)
</details>

---
<details>
<summary><span style="font-size:200%"> User Guide - Video </span></summary>

> * ### [Getting Start with AEDA](http://www.rfdh.com/pds/adea/Getting_Start_with_ADEA.mp4)
> * ### [Quick Guide for DQ Eye Analyze](http://www.rfdh.com/pds/adea/Quick_Guide_for_DQ_Eye_Analyze.mp4)
> * ### Quick Guide for IBIS Optimization
> ---
> * ### [Problem in Running ADEA](http://www.rfdh.com/pds/adea/Problem_in_Running_ADEA.mp4)
> * ### Select Version of Ansys Electronics Desktop
> * ### What is Deifnition File?
>   > * ### Modify and/or Add DDR Specifications
>   > * ### Automatic Net Classifications
>   > * ### Automatic IBIS Identification
> * ### What is Configuration File?
> * ### Analyze with 'Analyze Group'
</details>

---
<!-- ## History
> ### [v0.5.1] - '22.08.06
>>- ##### Eye 계측 Algorithm Classic Version(VB) 으로 변경 후, Excel report 생성 bug 수정
>>- ##### Resource 폴더 정리
>>- ##### 예제 Archive file 추가
>>- ##### CSV input disable

> ### [v0.5.2] - '22.08.07
>>- ##### Excel report format 변경
>>- ##### Jitter, Jitter_RMS 열 삭제
>>- ##### Width & Margin UI 단위 열 추가

> ### [v0.5.3] - '22.08.08
>>- ##### IBIS bug fix    
>>- ##### Show result window for each IBIS cases

> ### [v0.6] - '22.08.09
>>- ##### Release to SEC

> ### [v0.6.1] - '22.08.12
>>- ##### Modify IBIS Optimization example (buffer -> pin import)
>>- ##### Bug fix for IBIS New & pin import case

> ### [v0.6.2] - '22.08.24
>>- ##### IBIS Model check시 sim case 바로 반영되지 않던 문제 수정
>>- ##### IBIS Model refresh button click시 sim case 초기화 되지 않던 문제 수정
>>- ##### IBIS Run Click시 초기화 문제 수정
>>- ##### Tx/Rx 같은 *.ibs file 사용 Case update
>>- ##### IBIS form resize event update
>>- ##### Automatic data-rate detect algorithm are updated

> ### [v0.6.3] - '22.08.30
>>- ##### 이전 IBIS 형식으로 작성된 Schematic에서도 IBIS opt. 동작하도록 update.
>>- ##### 이전 IBIS 형식의 예제 Schematic update (LPDDR4_2133_IBIS_Example_for_Old_IBIS.aedtz)

> ### [v0.6.4] - '22.09.01
>>- ##### 예제 Archive file 재정비
>>- ##### 자동 Datarate 입력 기능 Disable
>>- ##### QC Routine 및 QC 결과표 작성

> ### [v0.6.5] - '22.09.16
>>- ##### 연속 해석 진행시, 이전 해석에서 설정했던 Report Export option이 초기화 되지 않는 문제 수정.
>>- ##### IBIS opt. 해석 진행 후, detailed report창에서 report export할 수 없도록 수정 -> 대신 전체 optimization 결과를 export할 수 있도록 update할 예정임.
>>- ##### IBIS opt. 해석 전 또는 해석 후 result 버튼 click하면 error 발생하던 문제 수정
>>- ##### Analysis Group 설정 하고 Eye 해석 진행 후, IBIS opt. 해석 진행하면 결과가 grouping되어 보이던 문제 수정
>>- ##### IBIS opt. 연속 수행하면, AEDT에서 Sim case가 누적되어 해석되던 문제 수정
>>- ##### Input file을 load 한 뒤, 새로운 file을 load 하려다 cancel 하면, 기존 입력되어 있던 design name이 삭제되던 현상 수정.
>>- ##### v0.6.5 기준 한글 + 영문 User manual, Quick Guide, Readme.md, Readme.html update.
>>- ##### GUI 에서 About ADEA Menu 다시 활성화 함.

> ### [v1.0] - '22.09.16
>>- ##### Release ADEA v1.0.

> ### [v1.0.1] - '22.09.26
>>- ##### hotfix ADEA v1.0.1
>>- ##### AEDT 실행 version 선택을 환경 변수를 참고하던 기존의 방식에서,
>>- ##### 사용자의 입력을 받아 선택하도록 변경함.
>>- ##### 2020 R1 이상 version에서만 ADEA를 사용할 수 있도록 설정.
>>- ##### PC에 설치되지 않은 Version을 선택할 경우
>>- ##### 기본 앱 설정에 따라 AEDT가 실행되도록 업데이트 하였음.
>>- ##### Excel report exporting error가 중국어 문제로 의심되어, UTF-8 encoding script 추가함.

> ### [v1.1] - '22.09.30
>>- ##### feature/IBIS_report ADEA v1.1
>>- ##### IBIS optimization 해석 결과를 Excel로 export할 수 있도록 Update.
>>- ##### 각 Case별 worst case eye-diagram 그림 포함 기능 추가
-->