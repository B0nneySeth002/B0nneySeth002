import java.util.Stack;

public class ExpressionChecker
{
   public boolean checkParentheses(String expression)  
   {
      Stack<String> stk = new Stack<String>();
      for (int i = 0; i < expression.length(); i++)
      {
         String part = expression.substring(i, i + 1);
         stk.push(part);
         if (part.equals(")")) {
            String top = stk.pop();
            while (!top.equals("(")) {
               if (stk.isEmpty()) {
                  return false;
               }
               top = stk.pop();
            }
         }
      }
      
      while (!stk.isEmpty())
      {
         String top = stk.pop();
         if (top.equals("(")) {
            return false;
         }
      }
      
      return true;
   }
}