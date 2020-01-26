//
//  TabBarController.swift
//  PresentationGeneratorSwift
//
//  Created by Tony Chen on 1/25/20.
//  Copyright © 2020 Tony. All rights reserved.
//

import UIKit

class TabBarController: UITabBarController {

    override func viewDidLoad() {
        super.viewDidLoad()
        

        
        let voice = ViewController()
        voice.setItem()
        voice.viewDidLoad()
        voice.tabBarItem.image = UIImage(systemName: "mic")
        voice.tabBarItem.selectedImage = UIImage(systemName: "mic")
        voice.tabBarItem.badgeColor = UIColor.black
        


        // Do any additional setup after loading the view.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
