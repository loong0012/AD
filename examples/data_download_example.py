#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据下载示例脚本
演示如何使用数据下载器下载阿尔兹海默症数据集
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_downloader import DataDownloader, download_real_data

def download_all_datasets():
    """下载所有数据集"""
    print("=== 下载所有阿尔兹海默症数据集 ===")
    
    # 使用便捷函数下载所有数据
    download_real_data(data_dir='./data')
    
def download_specific_datasets():
    """下载特定数据集"""
    print("=== 下载特定数据集 ===")
    
    # 创建数据下载器实例
    downloader = DataDownloader(data_dir='./data')
    
    # 创建目录结构
    downloader.create_real_data_directories()
    
    # 下载ADNI数据集
    print("\n下载ADNI数据集...")
    adni_dir = downloader.download_adni_sample()
    
    # 下载OASIS数据集
    print("\n下载OASIS数据集...")
    oasis_dir = downloader.download_oasis_data()
    
    # 下载Kaggle数据集
    print("\n下载Kaggle数据集...")
    kaggle_dir = downloader.download_kaggle_data()
    
    print("\n=== 下载完成 ===")
    print(f"ADNI数据目录: {adni_dir}")
    print(f"OASIS数据目录: {oasis_dir}")
    print(f"Kaggle数据目录: {kaggle_dir}")

def download_additional_datasets():
    """下载其他数据集"""
    print("=== 下载其他数据集 ===")
    
    downloader = DataDownloader(data_dir='./data')
    
    # 下载MIRIAD数据集
    print("\n下载MIRIAD数据集...")
    miriad_dir = downloader.download_miriad_data()
    
    # 下载NACC数据集
    print("\n下载NACC数据集...")
    nacc_dir = downloader.download_nacc_data()
    
    # 下载ADRC数据集
    print("\n下载ADRC数据集...")
    adrc_dir = downloader.download_adrc_data()
    
    # 下载UCSD数据集
    print("\n下载UCSD数据集...")
    ucsd_dir = downloader.download_ucsd_data()
    
    # 下载Harvard AD数据集
    print("\n下载Harvard AD数据集...")
    harvard_dir = downloader.download_harvard_data()
    
    print("\n=== 下载完成 ===")
    print(f"MIRIAD数据目录: {miriad_dir}")
    print(f"NACC数据目录: {nacc_dir}")
    print(f"ADRC数据目录: {adrc_dir}")
    print(f"UCSD数据目录: {ucsd_dir}")
    print(f"Harvard AD数据目录: {harvard_dir}")

def show_dataset_info():
    """显示数据集信息"""
    print("=== 阿尔兹海默症数据集信息 ===")
    print("\n可用数据集:")
    print("1. ADNI (Alzheimer's Disease Neuroimaging Initiative)")
    print("   - 包含MRI、PET、临床和分子数据")
    print("   - 网站: https://adni.loni.usc.edu/")
    
    print("\n2. OASIS (Open Access Series of Imaging Studies)")
    print("   - 包含MRI和临床数据")
    print("   - 网站: https://www.oasis-brains.org/")
    
    print("\n3. Kaggle Alzheimer's Dataset")
    print("   - 包含MRI影像数据")
    print("   - 网站: https://www.kaggle.com/tourist55/alzheimers-dataset-4-class-of-images")
    
    print("\n4. MIRIAD (Multi-modal MRI in Alzheimer's Disease)")
    print("   - 包含多模态MRI数据")
    print("   - 网站: https://fcon_1000.projects.nitrc.org/indi/retro/miriad.html")
    
    print("\n5. NACC (National Alzheimer's Coordinating Center)")
    print("   - 包含临床和神经心理学数据")
    print("   - 网站: https://naccdata.org/")
    
    print("\n6. ADRC (Alzheimer's Disease Research Center)")
    print("   - 包含临床和研究数据")
    print("   - 网站: https://adrc.loni.usc.edu/")
    
    print("\n7. UCSD BrainCode")
    print("   - 包含MRI和其他神经影像数据")
    print("   - 网站: https://braincode.ucsd.edu/")
    
    print("\n8. Harvard AD Dataset")
    print("   - 包含临床和研究数据")
    print("   - 网站: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/2614")

def main():
    """主函数"""
    print("阿尔兹海默症数据集下载示例")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 下载所有数据集")
        print("2. 下载基本数据集 (ADNI, OASIS, Kaggle)")
        print("3. 下载其他数据集")
        print("4. 显示数据集信息")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ")
        
        if choice == '1':
            download_all_datasets()
        elif choice == '2':
            download_specific_datasets()
        elif choice == '3':
            download_additional_datasets()
        elif choice == '4':
            show_dataset_info()
        elif choice == '5':
            print("退出程序...")
            break
        else:
            print("无效的选择，请重新输入")

if __name__ == '__main__':
    main()
