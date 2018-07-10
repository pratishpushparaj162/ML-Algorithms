#include <iostream>
#include<string>
using namespace std;

string fillarray(string arr, int n)
{
    int temp = 10;
    while (true)
    {
        int t = n%temp;
        arr = to_string((long long int)t) + arr;
        if (n < temp)
            break;
        n = n/temp;
    }
    return arr;
}

string factorial(string arr, int n, int back, int carry)
{
    if (n == 0)
        return arr;
    int temp = (arr[back] - 48) * n + carry;
    if (temp == 0 && back != arr.size()-1)
        return factorial(arr, n-1, arr.size()-1, 0);
    arr[back] = (temp%10);
    carry = temp/10;
    back --;
    return factorial(arr, n, back, carry);
}

void solve(int n)
{
    string arr;
    arr = fillarray(arr, n);
    arr = factorial(arr, n-1, arr.size()-1, 0);
    cout << arr << endl;
    return ;
}

int main(){
    int tc;
    cin >> tc;
    for (int t = 0; t < tc; t++)
    {
        int n;
        cin >> n;
        solve(n);
    }
    return 0;
}
