if($("#radiOpt0").is(":checked")){
         
    if(fifteenList != null && fifteenList.length > 0) {
          
          html += '<tr>';
          html +=    '<th class="text-center" width="14%">업체</th>';
          html +=    '<th class="text-center" width="14%">계측기명</th>';
          html +=    '<th class="text-center" width="14%">일자</th>';
          if($("#checkOpt0").is(":checked")){
             html += '<th class="text-center" width="14%" id="instantaneous">현재 유효전력<br>(kw:순시값)</th>';
          }
          if($("#checkOpt1").is(":checked")){
             html += '<th class="text-center" width="14%" id="rateValue">역률(%)</th>';
          }
          if($("#checkOpt2").is(":checked")){
             html += '<th class="text-center" width="14%" id="voltage">전압(V)</th>';
          }
          if($("#checkOpt3").is(":checked")){
             html += '<th class="text-center" width="14%" id="watt">전류값(A)</th>';
          }
          html += '</tr>';
          
       for(var i = 0; i< fifteenList.length; i++) {

          html2 += '<tr>';
          html2 +=    '<td class="text-center">'+ fifteenList[i].plantNm +'</td>'
          html2 +=    '<td class="text-center">'+ fifteenList[i].meterNm +'</td>';
          html2 +=    '<td class="text-center">'+ fifteenList[i].regDate +'</td>';
          if($("#checkOpt0").is(":checked")){
             html2 += '<td class="text-center">'+ parseFloat(fifteenList[i].instantaneous).toFixed(1) +'</td>';
          }
          if($("#checkOpt1").is(":checked")){
             html2 += '<td class="text-center">'+ parseFloat(fifteenList[i].rateValue).toFixed(1) +'</td>';
          }
          if($("#checkOpt2").is(":checked")){
             html2 += '<td class="text-center">'+ parseFloat(fifteenList[i].voltage).toFixed(1) +'</td>';
          }
          if($("#checkOpt3").is(":checked")){
             html2 += '<td class="text-center">'+ parseFloat(fifteenList[i].watt).toFixed(1) +'</td>';
          }
          html2 += '</tr>';
       }
 
    }else{
       html += '<tr>';
       html +=    '<th class="text-center" width="14%">업체</th>';
       html +=    '<th class="text-center" width="14%">계측기명</th>';
       html +=    '<th class="text-center" width="14%">일자</th>';
       html +=    '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
       html +=    '<th class="text-center" width="14%">역률(%)</th>';
       html +=    '<th class="text-center" width="14%">전압(V)</th>';
       html +=    '<th class="text-center" width="14%">전류값(A)</th>';
       html += '</tr>';
       
       html2 += '<tr height="100">';
       html2 += '   <td class="text-center" colspan="7">데이터가 없습니다</td>';         
       html2 += '</tr>';
    }
    
 }else if($("#radiOpt1").is(":checked")){
    
    if(thirtyList != null && thirtyList.length > 0) {
       
          html += '<tr>';
          html +=    '<th class="text-center" width="14%">업체</th>';
          html +=    '<th class="text-center" width="14%">계측기명</th>';
          html +=    '<th class="text-center" width="14%">일자</th>';
          if($("#checkOpt0").is(":checked")){
             html += '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
          }
          if($("#checkOpt1").is(":checked")){
             html += '<th class="text-center" width="14%">역률(%)</th>';
          }
          if($("#checkOpt2").is(":checked")){
             html += '<th class="text-center" width="14%">전압(V)</th>';
          }
          if($("#checkOpt3").is(":checked")){
             html += '<th class="text-center" width="14%">전류값(A)</th>';
          }
          html += '</tr>';
          
       for(var i = 0; i< thirtyList.length; i++) {

          html2 += '<tr>';
          html2 +=    '<td class="text-center">'+ thirtyList[i].plantNm +'</td>'
          html2 +=    '<td class="text-center">'+ thirtyList[i].meterNm +'</td>';
          html2 +=    '<td class="text-center">'+ thirtyList[i].regDate +'</td>';
          if($("#checkOpt0").is(":checked")){
             html2 += '<td class="text-center" id="instantaneous">'+ parseFloat(thirtyList[i].instantaneous).toFixed(1) +'</td>';
          }
          if($("#checkOpt1").is(":checked")){
             html2 += '<td class="text-center" id="rateValue">'+ parseFloat(thirtyList[i].rateValue).toFixed(1) +'</td>';
          }
          if($("#checkOpt2").is(":checked")){
             html2 += '<td class="text-center" id="voltage">'+ parseFloat(thirtyList[i].voltage).toFixed(1) +'</td>';
          }
          if($("#checkOpt3").is(":checked")){
             html2 += '<td class="text-center" id="watt">'+ parseFloat(thirtyList[i].watt).toFixed(1) +'</td>';
          }
          html2 += '</tr>';
       }

    }else{
       html += '<tr>';
       html +=    '<th class="text-center" width="14%">업체</th>';
       html +=    '<th class="text-center" width="14%">계측기명</th>';
       html +=    '<th class="text-center" width="14%">일자</th>';
       html +=    '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
       html +=    '<th class="text-center" width="14%">역률(%)</th>';
       html +=    '<th class="text-center" width="14%">전압(V)</th>';
       html +=    '<th class="text-center" width="14%">전류값(A)</th>';
       html += '</tr>';
       
       html2 += '<tr height="100">';
       html2 += '   <td class="text-center" colspan="7">데이터가 없습니다</td>';         
       html2 += '</tr>';
    }
    
 }else if($("#radiOpt2").is(":checked")){
    
    if(hourList != null && hourList.length > 0) {
       
          html += '<tr>';
          html +=    '<th class="text-center" width="14%">업체</th>';
          html +=    '<th class="text-center" width="14%">계측기명</th>';
          html +=    '<th class="text-center" width="14%">일자</th>';
          if($("#checkOpt0").is(":checked")){
             html += '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
          }
          if($("#checkOpt1").is(":checked")){
             html += '<th class="text-center" width="14%">역률(%)</th>';
          }
          if($("#checkOpt2").is(":checked")){
             html += '<th class="text-center" width="14%">전압(V)</th>';
          }
          if($("#checkOpt3").is(":checked")){
             html += '<th class="text-center" width="14%">전류값(A)</th>';
          }
          html += '</tr>';
          
       for(var i = 0; i< hourList.length; i++) {

          html2 += '<tr>';
          html2 +=    '<td class="text-center">'+ hourList[i].plantNm +'</td>'
          html2 +=    '<td class="text-center">'+ hourList[i].meterNm +'</td>';
          html2 +=    '<td class="text-center">'+ hourList[i].regDate +'</td>';
          if($("#checkOpt0").is(":checked")){
             html2 += '<td class="text-center" id="instantaneous">'+ parseFloat(hourList[i].instantaneous).toFixed(1) +'</td>';
          }
          if($("#checkOpt1").is(":checked")){
             html2 += '<td class="text-center" id="rateValue">'+ parseFloat(hourList[i].rateValue).toFixed(1) +'</td>';
          }
          if($("#checkOpt2").is(":checked")){
             html2 += '<td class="text-center" id="voltage">'+ parseFloat(hourList[i].voltage).toFixed(1) +'</td>';
          }
          if($("#checkOpt3").is(":checked")){
             html2 += '<td class="text-center" id="watt">'+ parseFloat(hourList[i].watt).toFixed(1) +'</td>';
          }
          html2 += '</tr>';
       }

    }else{
       html += '<tr>';
       html +=    '<th class="text-center" width="14%">업체</th>';
       html +=    '<th class="text-center" width="14%">계측기명</th>';
       html +=    '<th class="text-center" width="14%">일자</th>';
       html +=    '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
       html +=    '<th class="text-center" width="14%">역률(%)</th>';
       html +=    '<th class="text-center" width="14%">전압(V)</th>';
       html +=    '<th class="text-center" width="14%">전류값(A)</th>';
       html += '</tr>';
       
       html2 += '<tr height="100">';
       html2 += '   <td class="text-center" colspan="7">데이터가 없습니다</td>';         
       html2 += '</tr>';
    }
    
 }else if($("#radiOpt3").is(":checked")){
 
    if(dayList != null && dayList.length > 0) {
       
          html += '<tr>';
          html +=    '<th class="text-center" width="14%">업체</th>';
          html +=    '<th class="text-center" width="14%">계측기명</th>';
          html +=    '<th class="text-center" width="14%">일자</th>';
          if($("#checkOpt0").is(":checked")){
             html += '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
          }
          if($("#checkOpt1").is(":checked")){
             html += '<th class="text-center" width="14%">역률(%)</th>';
          }
          if($("#checkOpt2").is(":checked")){
             html += '<th class="text-center" width="14%">전압(V)</th>';
          }
          if($("#checkOpt3").is(":checked")){
             html += '<th class="text-center" width="14%">전류값(A)</th>';
          }
          html += '</tr>';
          
       for(var i = 0; i< dayList.length; i++) {

          html2 += '<tr>';
          html2 +=    '<td class="text-center">'+ dayList[i].plantNm +'</td>'
          html2 +=    '<td class="text-center">'+ dayList[i].meterNm +'</td>';
          html2 +=    '<td class="text-center">'+ dayList[i].regDate +'</td>';
          
          if($("#checkOpt0").is(":checked")){
             html2 += '<td class="text-center" id="instantaneous">'+ parseFloat(dayList[i].instantaneous).toFixed(1) +'</td>';
          }
          if($("#checkOpt1").is(":checked")){
             html2 += '<td class="text-center" id="rateValue">'+ parseFloat(dayList[i].rateValue).toFixed(1) +'</td>';
          }
          if($("#checkOpt2").is(":checked")){
             html2 += '<td class="text-center" id="voltage">'+ parseFloat(dayList[i].voltage).toFixed(1) +'</td>';
          }
          if($("#checkOpt3").is(":checked")){
             html2 += '<td class="text-center"id="watt">'+ parseFloat(dayList[i].watt).toFixed(1) +'</td>';
          }
          html2 += '</tr>';
       }

    }else{
       html += '<tr>';
       html +=    '<th class="text-center" width="14%">업체</th>';
       html +=    '<th class="text-center" width="14%">계측기명</th>';
       html +=    '<th class="text-center" width="14%">일자</th>';
       html +=    '<th class="text-center" width="14%">현재 유효전력<br>(kw:순시값)</th>';
       html +=    '<th class="text-center" width="14%">역률(%)</th>';
       html +=    '<th class="text-center" width="14%">전압(V)</th>';
       html +=    '<th class="text-center" width="14%">전류값(A)</th>';
       html += '</tr>';
       
       html2 += '<tr height="100">';
       html2 += '   <td class="text-center" colspan="7">데이터가 없습니다</td>';         
       html2 += '</tr>';
    }
 }