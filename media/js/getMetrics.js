$(document(){
 function getMetrics(type, goal, start, end) {
  $('#' + type + '_metrics div').html('<span><i class="icon-spinner icon-spin"></i></span><h4></h4>');
  var jsonurl = '/api/metrics.json?type=' + encodeURIComponent(type) + '&goal=' + encodeURIComponent(goal);
  if (typeof start != 'undefined' && typeof end != 'undefined')
   jsonurl += '&start=' + encodeURIComponent(start) + '&end=' + encodeURIComponent(end);
   var data = $.getJSON(jsonurl, function(data) {
    $('.ovbox .num').html('0');
    var total_visits = 0;
    var total_conversions = 0;
    for (var i in data.tabs) {
     var tab = data.tabs[i];
     total_visits += parseInt(tab.visits);
     total_conversions += parseInt(tab.conversions);
     $('#tab_' + tab.type + '_visits').html(add_commas(tab.visits));
     $('#tab_' + tab.type + '_conversions').html(add_commas(tab.conversions));
    }
    $('#tab_all_visits').html(add_commas(total_visits));
    $('#tab_all_conversions').html(add_commas(total_conversions));
    var url = '/reports/mywebshop/people';
    if (type != 'all')
     url += '?filters[' + type + ']=1';
    $('#' + type + '_metrics .people span').html('<a href="' + url + '">' + add_commas(data.people) + '</a>');
    $('#' + type + '_metrics .people h4').html('People');
    var url = '/reports/mywebshop/clicks';
    if (type != 'all')
     url += '?filters[' + type + ']=1';
    $('#' + type + '_metrics .clicks span').html('<a href="' + url + '">' + add_commas(data.clicks) + '</a>');
    $('#' + type + '_metrics .clicks h4').html((type == 'ad') ? 'Site Visits<br />(Ad Clicks)' : 'Site Visits');
    var url = '/reports/mywebshop/conversions?filters[goal]=' + encodeURIComponent(selected_goal);
    if (type != 'all')
     url += '&filters[' + type + ']=1';
    $('#' + type + '_metrics .conversions span').html('<a href="' + url + '">' + add_commas(data.conversions) + '</a>');
    $('#' + type + '_metrics .conversions h4').html('Goal Conversions');
    $('#' + type + '_metrics .convrate span').html(format_rate(data.conversions / data.people));
    $('#' + type + '_metrics .convrate h4').html('Conversion Rate');
    $('#' + type + '_metrics .revenue span').html(format_money(data.revenue));
    $('#' + type + '_metrics .revenue h4').html('Revenue');
    $('#' + type + '_metrics .goalvalue span').html(format_money(data.revenue / data.conversions));
    $('#' + type + '_metrics .goalvalue h4').html('Average Goal Value');
    $('#' + type + '_metrics .revperson span').html(format_money(data.revenue / data.people));
    $('#' + type + '_metrics .revperson h4').html('Revenue Per Person');
    if (type == 'all' || type == 'ad') {
     $('#' + type + '_metrics .cost span').html(format_money(data.cost));
     $('#' + type + '_metrics .cost h4').html('Cost');
     $('#' + type + '_metrics .profit span').html(format_money(data.revenue - data.cost));
     $('#' + type + '_metrics .profit h4').html('Profit');
     $('#' + type + '_metrics .costpergoal span').html(format_money(data.cost / data.conversions));
     $('#' + type + '_metrics .costpergoal h4').html('Cost Per Acquisition (CPA)');
    }
   });
   /* Graph */
   $('#' + type + '_graph').html('<div style="padding: 40px 0 0 0; text-align: center; font-size: 33px"><i class="icon-spinner icon-spin"></i></div>');
   var jsonurl = '/api/graph.json?graph=1&filters[goal]=' + encodeURIComponent(goal);
   if (type != 'all')
    jsonurl += '&filters[' + type + ']=1';
   if (typeof start != 'undefined' && typeof end != 'undefined')
    jsonurl += '&start=' + encodeURIComponent(start) + '&end=' + encodeURIComponent(end);
   $.getJSON(jsonurl, function(data) {
    var html = '', clicks = 0, people = 0, conversions = 0, revenue = 0;
     if (data.graph.length == 0) {
      $('#' + type + '_graph').html('No Data');
     } else {
      var people = [], conversions = [];
      for (var i in data.graph) {
       var row = data.graph[i];
       people.push([moment(row.date).valueOf(), parseInt(row.people)]);
       conversions.push([moment(row.date).valueOf(), parseInt(row.conversions)])
      }
     HighchartsGraph(type + '_graph', people, conversions, data.people, data.conversions);
    }
   });
  } 
 });