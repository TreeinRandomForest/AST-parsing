# def bubbleSort(self, nums):
#     n = len(nums)
#     for i in range(n):
#         for j in range(0, n - i - 1):
#             if nums[j] > nums[j + 1]:
#                 nums[j], nums[j + 1] = nums[j + 1], nums[j]
                
# def selection_sort(arr):        
#     for i in range(len(arr)):
#         minimum = i
#         for j in range(i + 1, len(arr)):
#             if arr[j] < arr[minimum]:
#                 minimum = j
#         arr[minimum], arr[i] = arr[i], arr[minimum]
        
def reverseArray(arr, start, end): 
    while (start < end): 
        arr[start], arr[end] = arr[end], arr[start] 
        start += 1
        end = end-1

def print_hello(a):
    if a == [1,2]:
        print ("hello")
    reverseArray(a)
    return a
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                