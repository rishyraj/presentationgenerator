//
//  TextViewController.swift
//  PresentationGeneratorSwift
//
//  Created by Tony Chen on 1/25/20.
//  Copyright © 2020 Tony. All rights reserved.
//

import UIKit

class TextViewController: UIViewController {
    
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
    
    
}
