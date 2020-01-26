//
//  TextViewController.swift
//  PresentationGeneratorSwift
//
//  Created by Tony Chen on 1/25/20.
//  Copyright © 2020 Tony. All rights reserved.
//

import UIKit
import MobileCoreServices

class TextViewController: UIViewController, UIDocumentPickerDelegate {
    
    
    @IBOutlet weak var textView: UITextView!
    @IBOutlet var titleLabel: UIView!
    @IBOutlet weak var uploadFile: UIButton!
    @IBOutlet weak var generateButton: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        textView.layer.borderWidth = 1.0
        textView.layer.borderColor = UIColor.lightGray.cgColor
        
        if (self.traitCollection.userInterfaceStyle == .dark) {
            titleLabel.tintColor = UIColor.white
            generateButton.tintColor = UIColor.white
            uploadFile.tintColor = UIColor.white
            textView.textColor = UIColor.white
        } else {
            titleLabel.tintColor = UIColor.black
            generateButton.tintColor = UIColor.black
            uploadFile.tintColor = UIColor.black
            textView.textColor = UIColor.black
        }
        
        let toolBar = UIToolbar()
        toolBar.sizeToFit()
        let doneButton = UIBarButtonItem(title: "Done", style: UIBarButtonItem.Style.done, target: self, action: #selector(self.dismissKeyboard))
        toolBar.setItems([doneButton], animated: true)
        
        textView.inputAccessoryView = toolBar
        
        
        
        // Do any additional setup after loading the view.
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
    
    @IBAction func selectFile(_ sender: Any) {
        let documentPicker = UIDocumentPickerViewController(documentTypes: [kUTTypePlainText as String], in: .import)
        documentPicker.delegate = self
        documentPicker.allowsMultipleSelection = false
        present(documentPicker, animated: true, completion: nil)
    }
    
    @IBAction func generatePresentation(_ sender: Any) {
        let url = URL(string: "http://127.0.0.1:5000/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
//        let postString = textView.text!
//        request.httpBody = postString.data(using: String.Encoding.utf8);
//
//        print(postString)
        
        let parameters: [String: Any] = [
            "rawtext": textView.text ?? ""
        ]
        request.httpBody = parameters.percentEncoded()
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
                
                // Check for Error
                if let error = error {
                    print("Error took place \(error)")
                    return
                }
         
                // Convert HTTP Response Data to a String
                if let data = data, let dataString = String(data: data, encoding: .utf8) {
                    print("Response data string:\n \(dataString)")
                }
        }
        task.resume()
    }
    
    
    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentAt url: URL) {
        print(url)
        do {
            let fileContent = try String(contentsOf: url, encoding: .utf8)
            textView.text = fileContent
            print(fileContent)
        } catch {
            return
        }
    }
    
    
}

extension ViewController: UIDocumentPickerDelegate {
    //    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentAt url: URL) {
    //        print(url)
    //    }
    
    //    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
    //        print(urls)
    //        do {
    //            let fileContent = try String(contentsOf: urls[1], encoding: .utf8)
    //            print(fileContent)
    //        } catch {
    //            return
    //        }
    //    }
}

extension Dictionary {
    func percentEncoded() -> Data? {
        return map { key, value in
            let escapedKey = "\(key)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            let escapedValue = "\(value)".addingPercentEncoding(withAllowedCharacters: .urlQueryValueAllowed) ?? ""
            return escapedKey + "=" + escapedValue
        }
        .joined(separator: "&")
        .data(using: .utf8)
    }
}

extension CharacterSet {
    static let urlQueryValueAllowed: CharacterSet = {
        let generalDelimitersToEncode = ":#[]@" // does not include "?" or "/" due to RFC 3986 - Section 3.4
        let subDelimitersToEncode = "!$&'()*+,;="

        var allowed = CharacterSet.urlQueryAllowed
        allowed.remove(charactersIn: "\(generalDelimitersToEncode)\(subDelimitersToEncode)")
        return allowed
    }()
}
