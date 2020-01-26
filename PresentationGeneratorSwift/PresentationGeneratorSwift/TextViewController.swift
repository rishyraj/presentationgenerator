//
//  TextViewController.swift
//  PresentationGeneratorSwift
//
//  Created by Tony Chen on 1/25/20.
//  Copyright © 2020 Tony. All rights reserved.
//

import UIKit
import MobileCoreServices
var responseMessage = ""

class TextViewController: UIViewController, UIDocumentPickerDelegate {
    
    
    @IBOutlet weak var textView: UITextView!
    @IBOutlet var titleLabel: UIView!
    @IBOutlet weak var uploadFile: UIButton!
    @IBOutlet weak var generateButton: UIButton!
    @IBOutlet weak var enterSpeechLabel: UILabel!
    
    func setItem() {
        self.title = "Text Input"
        self.tabBarItem.image = UIImage(systemName: "doc.text")
        self.tabBarItem.selectedImage = UIImage(systemName: "doc.text")
        self.tabBarItem.badgeColor = UIColor.black
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.title = "Text Input"
        self.tabBarItem.image = UIImage(systemName: "doc.text")
        self.tabBarItem.selectedImage = UIImage(systemName: "doc.text")
        self.tabBarItem.badgeColor = UIColor.black
        
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
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
    
    @IBAction func selectFile(_ sender: Any) {
        clearFields(self)
        let documentPicker = UIDocumentPickerViewController(documentTypes: [kUTTypePlainText as String], in: .import)
        documentPicker.delegate = self
        documentPicker.allowsMultipleSelection = false
        present(documentPicker, animated: true, completion: nil)
    }
    
    @IBAction func generatePresentation(_ sender: Any) {
        let url = URL(string: "http://127.0.0.1:5000/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
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
                DispatchQueue.main.async {
                    self.textView.text = dataString
                    self.enterSpeechLabel.text = "HERE IS YOUR LINK!"
                }
            }
        }
        task.resume()
        
    }
    
    
    func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentAt url: URL) {
        print(url)
        do {
            let fileContent = try String(contentsOf: url, encoding: .utf8)
            textView.text = fileContent
        } catch {
            return
        }
    }
    
    
    @IBAction func clearFields(_ sender: Any) {
        self.textView.text = ""
        self.enterSpeechLabel.text = "Enter Speech or Upload Text"
    }
    
    
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
