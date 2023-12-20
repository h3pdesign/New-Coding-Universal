function createWidget(json){
  let w = new ListWidget()
  w.backgroundColor = new Color("#1A202C")
  w.addSpacer(1)
  
  let locationTxt = w.addText(json[2])
  locationTxt.font = Font.regularRoundedSystemFont(14)
  locationTxt.textColor = new Color("#AAAAAA")
  
  let titleTxt = w.addText(json[0])
  titleTxt.font = Font.boldRoundedSystemFont(17)
  titleTxt.textColor = new Color("#FFFFFF")
  
  let statusTxt = w.addText(json[1])
  statusTxt.font = Font.regularRoundedSystemFont(14)
  statusTxt.textColor = new Color("#AAAAAA")

  return w
}

async function loadItems() {
  let url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"
  let req = new Request(url)
  let json = await req.loadJSON()
  json = json.results[0]
  let name = json.name
  let status = json.status.name
  let location = json.pad.location.name
  let info = [name, status, location]
  return info
}

let data = await loadItems()

let w = createWidget(data)
Script.setWidget(w)
if(config.runsInApp){
  w.presentMedium() 
  
}
