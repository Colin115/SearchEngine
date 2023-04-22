let sharedDefaults = UserDefaults(suiteName: Bundle.main.object(forInfoDictionaryKey: "ApplicationGroupPlistKey") as! String)

StandardRequestor.request(withInfo: info, httpMethod: "POST", path: USERRESPONSEROUTE, sharedDefaults: sharedDefaults) { (responseInfo, responseStatus, error) in 
  if let error = error, responseStatus != 200 {
    // Handle the error and response status here
  } else {
    // Handle the response info here
  }

  StandardRequestor.sendRequest(with: request, onCompletion: { (responseInfo, responseStatus, error) in
    // Handle the response info or errors here, if needed
  })
}
