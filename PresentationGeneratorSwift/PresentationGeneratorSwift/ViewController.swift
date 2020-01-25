//
//  ViewController.swift
//  PresentationGeneratorSwift
//
//  Created by Tony Chen on 1/25/20.
//  Copyright © 2020 Tony. All rights reserved.
//

import UIKit
import AVFoundation

class ViewController: UIViewController {
    
    @IBOutlet weak var recordButton: UIButton!
    @IBOutlet weak var generateButton: UIButton!
    var recordingSession: AVAudioSession!
    var audioRecorder: AVAudioRecorder!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        if (self.traitCollection.userInterfaceStyle == .dark) {
            recordButton.tintColor = UIColor.white
            generateButton.tintColor = UIColor.white
        } else {
            recordButton.tintColor = UIColor.black
            generateButton.tintColor = UIColor.black
        }
        
    }


}

