//
//  ViewController.swift
//  PresentationGeneratorSwift
//
//  Created by Tony Chen on 1/25/20.
//  Copyright © 2020 Tony. All rights reserved.
//

import UIKit
import AVFoundation
import MobileCoreServices
import Alamofire

class ViewController: UIViewController, AVAudioRecorderDelegate {
    
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
        
        recordButton.isHidden = true
        
        recordingSession = AVAudioSession.sharedInstance()
        
        do {
            try recordingSession.setCategory(.playAndRecord, mode: .default)
            try recordingSession.setActive(true)
            recordingSession.requestRecordPermission() { [unowned self] allowed in
                DispatchQueue.main.async {
                    if allowed {
                        self.recordButton.isHidden = false
                        print("good to go")
                    } else {
                        // failed to record!
                        print("can't record")
                    }
                }
            }
        } catch {
            // failed to record!
            print("cant record")
        }
        
    }
    
    func startRecording() {
        let audioFilename = getDocumentsDirectory().appendingPathComponent("sound.flac")
        
        let settings = [
            AVFormatIDKey: Int(kAudioFormatFLAC),
            AVSampleRateKey: 16000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        do {
            audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            audioRecorder.delegate = self
            audioRecorder.record()
            
            recordButton.setBackgroundImage(UIImage(systemName: "mic.circle.fill"), for: .normal)
        } catch {
            finishRecording(success: false)
        }
    }
    
    func finishRecording(success: Bool) {
        
        audioRecorder.stop()
        audioRecorder = nil
        
        if success {
            recordButton.setBackgroundImage(UIImage(systemName: "mic.circle"), for: .normal)
        } else {
            recordButton.setBackgroundImage(UIImage(systemName: "mic.circle"), for: .normal)
            print("record failed")
        }
    }
    
    func getDocumentsDirectory() -> URL {
        let paths = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)
        return paths[0]
    }
    
    func audioRecorderDidFinishRecording(_ recorder: AVAudioRecorder, successfully flag: Bool) {
        if !flag {
            finishRecording(success: false)
        }
    }
    
    
    
    @IBAction func recordTapped(_ sender: Any) {
        print("tapped")
        if audioRecorder == nil {
            print("starting\n")
            startRecording()
        } else {
            print("stopping")
            finishRecording(success: true)
        }
    }
    
    
    @IBAction func generate(_ sender: Any) {
        print("here")
        
        
        
        //        let requestUrl:URL = URL(string: "http://127.0.0.1:5000/")!
        //        var request = URLRequest(url: requestUrl)
        //        request.httpMethod = "POST"
        //        request.httpBodyStream = InputStream(url: getDocumentsDirectory())
        //
        //        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
        //
        //            if let error = error {
        //                print("failed")
        //                return
        //            }
        //
        //            if let data = data, let dataString = String(data: data, encoding: .utf8) {
        //                print("Response data string:\n \(dataString)")
        //            }
        //        }
        //        task.resume()
        
        let recordingURL = getDocumentsDirectory().appendingPathComponent("sound.flac")
        let url = "http://127.0.0.1:5000/"
        
        AF.upload(multipartFormData: { (multipartFormData) in
            multipartFormData.append(recordingURL, withName: "sound.flac")
        }, to: url).responseJSON { (response) in
            debugPrint(response)
        }
    }
    
    
    
}

